def lift_constants_pass(
    gm: torch.fx.GraphModule,
    graph_signature: ExportGraphSignature,
    constant_attrs: ConstantAttrMap,
) -> dict[str, Union[torch.Tensor, torch.ScriptObject, FakeScriptObject]]:
    """
    Takes a graph module, graph signature, and modifies them implace to lift any
    constants (tensors or custom classes) as inputs to the graph. Returns a
    dictionary of names to constants.

    Arguments:
        gm (torch.fx.GraphModule): The graph module containing the graph and constants to lift.
        graph_signature (ExportGraphSignature): This graph signature will be
            mutated to add additional CONSTANT_TENSOR and CUSTOM_OBJ inputs.
        constant_attrs (ConstantAttr): A mapping from a constant value to its
            fully-qualified path in `gm`. This is used to maintain consistent
            location of constants between the original module and the exported
            version.

    Returns:
        A dictionary of fqn => constant value.
    """
    all_constants: dict[
        str, Union[torch.Tensor, torch.ScriptObject, FakeScriptObject]
    ] = {}

    inputs = graph_signature.input_specs
    num_custom_obj = sum(
        input_specs.kind == InputKind.CUSTOM_OBJ for input_specs in inputs
    )
    num_tensor_constants = sum(
        input_specs.kind == InputKind.CONSTANT_TENSOR for input_specs in inputs
    )

    fake_mode = detect_fake_mode(
        tuple(node.meta["val"] for node in gm.graph.nodes if node.op == "placeholder")
    )

    first_user_input_loc, first_user_input = 0, next(iter(gm.graph.nodes))
    for node in gm.graph.nodes:
        if node.op == "placeholder":
            if node.name in graph_signature.user_inputs:
                first_user_input = node
                break
            first_user_input_loc += 1
        # If we ever hit here, it means that
        # there was no user input so the constants
        # should be inserted right before the first
        # non-placeholder node.
        if node.op != "placeholder":
            first_user_input = node
            break

    lifted_objs = ConstantAttrMap()
    renamed_targets = {}
    for node in gm.graph.nodes:
        if node.op == "get_attr":
            constant_val = _get_attr(gm, node.target)
            if constant_val in lifted_objs:
                # We already lifted this constant elsewhere. Just rewrite uses
                # of this get_attr to point to the already-existing placeholder
                # node.
                const_placeholder_node = _get_first_fqn(lifted_objs, constant_val)
                node.replace_all_uses_with(const_placeholder_node)
                gm.graph.erase_node(node)
                renamed_targets[node.name] = const_placeholder_node.name
                continue

            # For ScriptObject, Tensor and FakeScriptObject constants:
            # First check if the constant was an attribute on some module by
            # consulting `constant_attrs` map. If it is, use the fqn that keeps
            # its location consistent with the eager module.
            #
            # If it's not in the `constant_attrs` map, that means it's an inline
            # constant (e.g. x + torch.tensor(0)), and thus did not have a
            # specific location in the eager module. In that case, just generate
            # some name and attach it to the module in which it was used.
            if isinstance(constant_val, (torch.ScriptObject, FakeScriptObject)):
                constant_kind = InputKind.CUSTOM_OBJ
                constant_fqn = _get_first_fqn(constant_attrs, constant_val)
                if constant_fqn is not None:
                    constant_name = constant_fqn.replace(".", "_")
                else:
                    constant_name = f"lifted_custom_{num_custom_obj}"
                    constant_fqn = get_constant_fqn(node, constant_name)
                    num_custom_obj += 1
            elif isinstance(constant_val, torch.Tensor):
                # Remove the parameterness of constant_val
                if isinstance(constant_val, torch.nn.Parameter):
                    warnings.warn(
                        f"{node.target} created when tracing {node.meta.get('stack_trace', '<unknown stack>')} is a parameter. But"
                        f"it's not registered with register_parameter(). export will treat it as a constant tensor"
                    )
                    # We get the real data out of the parameter by disabling the surrounding fake mode.
                    with unset_fake_temporarily():
                        constant_val = constant_val.data
                constant_kind = InputKind.CONSTANT_TENSOR
                constant_fqn = _get_first_fqn(constant_attrs, constant_val)
                if constant_fqn is not None:
                    constant_name = constant_fqn.replace(".", "_")
                else:
                    constant_name = f"lifted_tensor_{num_tensor_constants}"
                    constant_fqn = get_constant_fqn(node, constant_name)
                    num_tensor_constants += 1
            elif isinstance(constant_val, torch.fx.GraphModule):
                continue
            elif "LoweredBackendModule" in type(constant_val).__name__:
                continue
            else:
                raise SpecViolationError(
                    f"getattr node {node} referencing unsupported type {type(constant_val)}"
                )

            with gm.graph.inserting_before(first_user_input):
                # Insert the constant node before the first user input
                const_placeholder_node = gm.graph.placeholder(constant_name)
                # match target name with its node name in case there is name collision
                # and suffix is added to node name in fx
                const_placeholder_node.target = const_placeholder_node.name

                for k, v in node.meta.items():
                    const_placeholder_node.meta[k] = v

                # Once the FQN has been used, remove nn_module_stack, stack_trace
                const_placeholder_node.meta.pop("nn_module_stack")
                const_placeholder_node.meta.pop("stack_trace", None)

                input_spec_arg: ArgumentSpec
                if isinstance(constant_val, torch.Tensor):
                    if fake_mode is not None:
                        const_placeholder_node.meta["val"] = fake_mode.from_tensor(
                            constant_val, static_shapes=True
                        )
                        const_placeholder_node.meta["val"].constant = constant_val
                    else:
                        const_placeholder_node.meta["val"] = constant_val
                    input_spec_arg = TensorArgument(name=const_placeholder_node.name)
                elif isinstance(constant_val, torch._C.ScriptObject):
                    class_fqn = constant_val._type().qualified_name()  # type: ignore[attr-defined]
                    const_placeholder_node.meta["val"] = CustomObjArgument(
                        constant_fqn, class_fqn
                    )
                    input_spec_arg = CustomObjArgument(
                        name=const_placeholder_node.name, class_fqn=class_fqn
                    )
                elif isinstance(constant_val, FakeScriptObject):
                    class_fqn = constant_val.script_class_name
                    const_placeholder_node.meta["val"] = CustomObjArgument(
                        constant_fqn, class_fqn, constant_val
                    )
                    input_spec_arg = CustomObjArgument(
                        name=const_placeholder_node.name,
                        class_fqn=class_fqn,
                        fake_val=constant_val,
                    )
                else:
                    raise SpecViolationError(
                        f"tried to lift unsupported type {type(constant_val)} from node {node.format_node()}"
                    )

                lifted_objs.add(constant_val, const_placeholder_node)
                node.replace_all_uses_with(const_placeholder_node)
                gm.graph.erase_node(node)

                renamed_targets[node.name] = const_placeholder_node.name

                # Add the constant as a buffer to the graph signature
                graph_signature.input_specs.insert(
                    first_user_input_loc,
                    InputSpec(
                        kind=constant_kind,
                        arg=input_spec_arg,
                        target=constant_fqn,
                    ),
                )
                if constant_val in constant_attrs:
                    for fqn in constant_attrs[constant_val]:
                        all_constants[fqn] = constant_val
                else:
                    all_constants[constant_fqn] = constant_val
                first_user_input_loc += 1

    for spec in graph_signature.output_specs:
        if spec.arg.name in renamed_targets:
            spec.arg.name = renamed_targets[spec.arg.name]

    return all_constants
