def rewrite_signature(
    f_sig,
    graph,
    fake_mode,
    flat_args,
    in_spec,
    example_fake_inputs,
    graph_captured_input,
    graph_captured_output,
    dynamo_traced_result,
    flat_args_dynamic_dims,
):
    orig_args, orig_kwargs = pytree.tree_unflatten(flat_args, in_spec)

    def check_user_input_output(flat_values, error_type):
        supported_types = [
            torch.Tensor,
            torch.SymInt,
            torch.SymFloat,
            torch.SymBool,
            torch._C.ScriptObject,
        ] + list(common_constant_types)

        def is_supported_type(val):
            return isinstance(val, tuple(supported_types))

        value_type = "input" if error_type == UserErrorType.INVALID_INPUT else "output"
        # We only check that the outputs are not None. Inputs can be None.
        for v in flat_values:
            if not is_supported_type(v):
                if error_type == UserErrorType.INVALID_INPUT and v is None:
                    continue

                raise UserError(
                    error_type,
                    f"It looks like one of the {value_type}s with type `{type(v)}` "
                    "is not supported or pytree-flattenable. \n"
                    f"Exported graphs {value_type}s can only contain the "
                    f"following supported types: {supported_types}. \n"
                    "If you are using a custom class object, "
                    "please register a pytree_flatten/unflatten function "
                    "using `torch.utils._pytree.register_pytree_node` or "
                    "`torch.export.register_dataclass`.",
                )

    check_user_input_output(flat_args, UserErrorType.INVALID_INPUT)
    flat_results_traced, out_spec_traced = pytree.tree_flatten(dynamo_traced_result)
    check_user_input_output(flat_results_traced, UserErrorType.INVALID_OUTPUT)

    def check_optional_input_and_error(f_sig: inspect.Signature):
        # Check if function has optional input.
        for name, param in f_sig.parameters.items():
            if param.default is not inspect.Parameter.empty:
                from torch._dynamo.exc import Unsupported

                log.error(
                    "Parameter %s is optional with a default value of %s",
                    name,
                    param.default,
                )
                raise Unsupported(
                    "Tracing through optional input is not supported yet",
                    case_name="optional_input",
                )

    def produce_matching(debug_type, sources, candidates):
        matched_elements_positions: list[Optional[int]] = []
        dict_of_source_vals = {}
        for i, val in enumerate(sources):
            dict_of_source_vals[id(val)] = i

        for i, val in enumerate(candidates):
            if isinstance(val, tuple(common_constant_types)):
                matched_elements_positions.append(None)
            elif id(val) not in dict_of_source_vals:
                if debug_type == "inputs":
                    check_optional_input_and_error(f_sig)
                raise AssertionError(
                    f"Unexpectedly found a {type(val)} in the {debug_type}.\n"
                    'Please file an issue along with a paste of the logs from TORCH_LOGS="+export"',
                )
            else:
                matched_elements_positions.append(dict_of_source_vals[id(val)])

        return matched_elements_positions

    matched_input_elements_positions = produce_matching(
        "inputs", flat_args, graph_captured_input
    )

    assert graph_captured_output is not None
    matched_output_elements_positions = produce_matching(
        "outputs", list(graph_captured_output) + flat_args, flat_results_traced
    )

    new_graph = FlattenInputOutputSignature(
        graph,
        flat_args,
        matched_input_elements_positions,
        flat_results_traced,
        matched_output_elements_positions,
        example_fake_inputs,
        flat_args_dynamic_dims,
        fake_mode,
    ).transform()

    # Make dynamo graph to have same input/output spec as user code
    def argument_names(f_sig, args, kwargs) -> list[str]:
        def signature_to_fullargspec(sig: inspect.Signature):
            # Get a list of Parameter objects from the Signature object
            params = list(sig.parameters.values())
            # Separate positional arguments, keyword-only arguments and varargs/varkw
            args = [
                p.name
                for p in params
                if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            ]
            kwonlyargs = [
                p.name for p in params if p.kind == inspect.Parameter.KEYWORD_ONLY
            ]
            varargs = next(
                (p.name for p in params if p.kind == inspect.Parameter.VAR_POSITIONAL),
                None,
            )
            varkw = next(
                (p.name for p in params if p.kind == inspect.Parameter.VAR_KEYWORD),
                None,
            )
            # Get default values for positional arguments and keyword-only arguments
            defaults = tuple(
                p.default
                for p in params
                if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
                and p.default is not inspect.Parameter.empty
            )
            kwonlydefaults = {
                p.name: p.default
                for p in params
                if p.kind == inspect.Parameter.KEYWORD_ONLY
                and p.default is not inspect.Parameter.empty
            }
            # Get annotations for parameters and return value
            annotations = {}
            if sig.return_annotation:
                annotations = {"return": sig.return_annotation}
            for parameter in params:
                annotations[parameter.name] = parameter.annotation
            # Return a FullArgSpec object with the extracted attributes
            return inspect.FullArgSpec(
                args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations
            )

        fullargspec = signature_to_fullargspec(f_sig)

        # 1. Map `args` 1-to-1 to positional arguments in original signature.
        input_strs = fullargspec.args[: len(args)]

        if len(args) > len(fullargspec.args):
            # 2. If there are more arguments left in `args`, they map to varargs in original
            # signature. Assign names as {varargs}_0, {varargs}_1, ...
            assert fullargspec.varargs is not None, "More arguments than expected"
            input_strs += [
                f"{fullargspec.varargs}_{i}"
                for i in range(0, len(args) - len(input_strs))
            ]
        elif len(args) < len(fullargspec.args):
            # 3. If there are fewer arguments in `args` than `fullargspec.args`,
            # it implies these are arguments either with default values, or provided in
            # `kwargs`. The former can be safely ignored. Because Dynamo.export does not
            # export them as part of the function signature. The latter will be handled
            # in the next step.
            for unprovided_arg in fullargspec.args[
                len(args) : -len(fullargspec.defaults or [])
            ]:
                assert unprovided_arg in kwargs, f"Missing argument {unprovided_arg}"

        # 4. Keyword arguments provided in `kwargs`.
        input_strs += list(kwargs.keys())

        # 5. Keyword-only arguments with default values if not provided are not exported
        # as part of the function signature.
        for kwonly_arg in fullargspec.kwonlyargs:
            kwonlydefaults = fullargspec.kwonlydefaults or {}
            assert kwonly_arg in kwargs or kwonly_arg in kwonlydefaults, (
                f"Missing keyword only argument {kwonly_arg}"
            )

        return input_strs

    new_graph.graph._codegen = _PyTreeCodeGen(
        _PyTreeInfo(
            argument_names(f_sig, orig_args, orig_kwargs),
            in_spec,
            out_spec_traced,
        )
    )
    new_graph.recompile()
    return new_graph
