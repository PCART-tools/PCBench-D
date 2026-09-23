def normalize(mod: torch.fx.GraphModule, expect_nodes_have_shapes: bool = False):
    assert len(_normalization_dict) > 0
    graph = mod.graph

    # For "call_module" node we return _base_class_origin if it's a
    # RewrittenModule, otherwise, return its type. For other nodes,
    # we return node.target.
    def get_target(mod: torch.fx.GraphModule, node: torch.fx.Node):
        if node.op != "call_module":
            return node.target

        # Find the module that node.target points to
        m = dict(mod.named_modules())[node.target]
        return getattr(m, "_base_class_origin", type(m))

    def normalize_to_acc_op(
        node: torch.fx.Node,
        normalization_info: NormalizationInfo,
        normalized_args: Tuple[Any, ...],
        normalized_kwargs: Dict[str, Any],
    ):
        # If there's a custom mapping function then use it.
        if normalization_info.custom_mapping_fn is not None:
            # For custom mapping, the normalized_kwargs are used for the original op,
            # i.e. *before* custom acc_ops normalization. Do that now.
            node.args = normalized_args
            node.kwargs = normalized_kwargs
            new_node = normalization_info.custom_mapping_fn(node, mod)
            # If a new node is returned then use it to replace the old node. Otherwise
            # the custom mapping function did its own replacement, so return early.
            if new_node is None:
                return
        else:
            # If there's kwargs_to_move_to_acc_out_ty then use it to setup acc_out_ty in
            # normalized_kwargs, and remove the kwarg from normalized_kwargs.
            move_kwargs_to_acc_out_ty(normalization_info, normalized_kwargs)

            # All acc ops are functions. Create a call to the correct acc_ops target using
            # the normalized kwargs provided.
            with graph.inserting_before(node):
                new_node = graph.create_node(
                    "call_function",
                    normalization_info.new_fn_target,
                    args=normalized_args,
                    kwargs=normalized_kwargs,
                    name=node.name,
                )
                new_node.meta = node.meta.copy()

        # Finally replace the original node with the normalized node.
        node.replace_all_uses_with(new_node)
        graph.erase_node(node)

    for node in graph.nodes:
        if node.op in {"placeholder", "get_attr", "output"}:
            continue

        normalization_info = _normalization_dict.get((node.op, get_target(mod, node)))

        # Also check if the torch_packaged version of the op was specified to be normalized.
        if normalization_info is None and node.op == "call_function":
            # Strip off the mangle_index suffix here before checking the map.
            target = re.sub(
                r"\A<torch_package_\d+>",
                "<torch_package_>",
                _get_qualified_name(node.target),
            )
            torch_package_op_and_target = (node.op, target)
            normalization_info = _normalization_dict.get(torch_package_op_and_target)

        if normalization_info is None:
            continue

        # Get the normalized kwargs to be used by normalize_to_acc_op below. If
        # normalization_info.arg_replacement_tuples is empty then assume the function
        # signature must be left as is.
        assert normalization_info.arg_replacement_tuples is not None
        if len(normalization_info.arg_replacement_tuples) == 0:
            normalized_args = node.args
            normalized_kwargs = node.kwargs
        else:
            normalized_args = ()
            try:
                normalized_kwargs = get_normalized_kwargs(
                    node, normalization_info.arg_replacement_tuples
                )
            except Exception:
                print(
                    f"Error during kwarg normalization for: {node.format_node()}; "
                    f"arg_replacement_tuples={normalization_info.arg_replacement_tuples}"
                )
                raise

        if (
            normalization_info.needs_shapes_for_normalization
            and not expect_nodes_have_shapes
        ):
            # All nodes needing shapes for normalization should be custom mapped.
            assert normalization_info.custom_mapping_fn is not None
            # For custom mapping, the normalized_kwargs are used for the original op,
            # i.e. *before* custom acc_ops normalization. Do that now so that whoever
            # consumes the graph next (e.g. shape inference) can use kwargs safely.
            node.args = normalized_args
            node.kwargs = normalized_kwargs
            continue

        try:
            normalize_to_acc_op(
                node, normalization_info, normalized_args, normalized_kwargs
            )
        except Exception:
            print(f"Error during normalization for node: {node.format_node()}")
            raise

    # If there are any dead nodes left after normalization, eliminate them now.
    mod.graph.eliminate_dead_code()
