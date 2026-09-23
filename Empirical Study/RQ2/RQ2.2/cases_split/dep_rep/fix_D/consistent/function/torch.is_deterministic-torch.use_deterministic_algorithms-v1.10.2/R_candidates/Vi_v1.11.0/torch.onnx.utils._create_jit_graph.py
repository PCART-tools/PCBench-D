def _create_jit_graph(model, args):
    torch_out = None
    params: Union[List, Tuple]
    if isinstance(model, torch.jit.ScriptModule):
        try:
            graph = model.forward.graph
            torch._C._jit_pass_onnx_function_substitution(graph)
            freezed_m = torch._C._freeze_module(model._c, preserveParameters=True)
            module, params = torch._C._jit_onnx_list_model_parameters(freezed_m)
            method_graph = module._get_method("forward").graph
            args_params = tuple(args) + tuple(params)
            param_count_list = _get_param_count_list(method_graph, args_params)
            in_vars, _ = torch.jit._flatten(args_params)
            graph = _propagate_and_assign_input_shapes(
                method_graph, tuple(in_vars), param_count_list, False, False)
        except AttributeError as e:
            raise RuntimeError("'forward' method must be a script method") from e
        return graph, params, torch_out, module
    elif isinstance(model, torch.jit.ScriptFunction):
        params = ()
        in_vars, in_desc = torch.jit._flatten(tuple(args))
        graph = model.graph
        torch._C._jit_pass_onnx_function_substitution(graph)
        param_count_list = _get_param_count_list(graph, args)
        graph = _propagate_and_assign_input_shapes(
            graph, tuple(in_vars), param_count_list, False, False)
        return graph, params, torch_out, None
    else:
        graph, torch_out = _trace_and_get_graph_from_model(model, args)
        torch._C._jit_pass_onnx_lint(graph)
        state_dict = _unique_state_dict(model)
        params = list(state_dict.values())
        graph_inputs = list(graph.inputs())
        user_input_num = len(graph_inputs) - len(state_dict)
        param_names = list(state_dict.keys())
        for i, inp in enumerate(graph_inputs):
            if i >= user_input_num:
                inp.setDebugName(param_names[i - user_input_num])
        torch._C._jit_pass_onnx_function_substitution(graph)
        return graph, params, torch_out, None
