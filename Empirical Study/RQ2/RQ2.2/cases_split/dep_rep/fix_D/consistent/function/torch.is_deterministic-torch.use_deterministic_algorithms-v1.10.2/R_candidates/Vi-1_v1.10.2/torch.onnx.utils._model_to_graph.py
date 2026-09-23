def _model_to_graph(model, args, verbose=False,
                    input_names=None, output_names=None,
                    operator_export_type=OperatorExportTypes.ONNX,
                    example_outputs=None, do_constant_folding=True,
                    _disable_torch_constant_prop=False, fixed_batch_size=False,
                    training=None, dynamic_axes=None):
    r"""Converts model into an ONNX graph.

    Returns:
      graph (torch._C.Graph): A TorchScript IR Graph with ONNX nodes.
      params_dict (Dict[str, torch.Tensor]): Dict from input param name to param value.
      torch_out (Union[NoneType, torch.Tensor, Tuple[torch.Tensor], List[torch.Tensor]]):
        The output tensors resulting from the trace of ``model``.
        If ``model`` is a :class:`torch.jit.ScriptModule` or :class:`torch.jit.ScriptFunction`,
        this will be None, since we are not doing any tracing.
    """
    # TODO: can we simplify this to always return a tuple of Tensor or None?
    from torch.onnx.symbolic_helper import _export_onnx_opset_version
    # Special case for common case of passing a single Tensor
    if isinstance(args, (torch.Tensor, int, float, bool)):
        args = (args, )

    graph, params, torch_out, module = _create_jit_graph(model, args)

    params_dict = _get_named_param_dict(graph, params)

    graph = _optimize_graph(graph, operator_export_type,
                            _disable_torch_constant_prop=_disable_torch_constant_prop,
                            fixed_batch_size=fixed_batch_size, params_dict=params_dict,
                            dynamic_axes=dynamic_axes, input_names=input_names,
                            module=module)
    from torch.onnx.symbolic_helper import _onnx_shape_inference
    if isinstance(model, torch.jit.ScriptModule) or isinstance(model, torch.jit.ScriptFunction):
        if example_outputs is None:
            example_outputs = _get_example_outputs(model, args)
        else:
            # example_outpus specified
            if isinstance(example_outputs, (torch.Tensor, int, float, bool)):
                example_outputs = (example_outputs,)

            if isinstance(example_outputs, list):
                example_outputs = [example_outputs]

        out_vars, desc = torch.jit._flatten(tuple(example_outputs))
        torch._C._jit_pass_onnx_assign_output_shape(graph, out_vars, desc, _onnx_shape_inference)
    else:
        flatten_args, _ = torch._C._jit_flatten(args)
        # make sure that the param dict and the graph match each other
        assert len(params) + len(flatten_args) == sum(1 for _ in graph.inputs())

    # NB: ONNX requires complete information about output types, which might be
    # erased by some optimizations, so we need to set it explicitly again.
    if torch_out is not None:
        if not (isinstance(torch_out, list) or isinstance(torch_out, tuple)):
            output_wrapped = [torch_out]
        else:
            output_wrapped = torch_out  # type: ignore[assignment]

        output_tensors, out_desc = torch._C._jit_flatten(tuple(output_wrapped))
        torch._C._jit_pass_onnx_assign_output_shape(graph, output_tensors, out_desc, _onnx_shape_inference)

    _set_input_and_output_names(graph, input_names, output_names)

    # make sure that the param dict and the graph match each other
    flatten_args, _ = torch._C._jit_flatten(args)
    assert len(params) + len(flatten_args) == sum(1 for _ in graph.inputs())

    params_dict = _get_named_param_dict(graph, params)

    if training is None or training == TrainingMode.EVAL:
        params_dict = torch._C._jit_pass_onnx_eval_peephole(graph, params_dict)

    if do_constant_folding and _export_onnx_opset_version in torch.onnx.constant_folding_opset_versions:
        params_dict = torch._C._jit_pass_onnx_constant_fold(graph, params_dict,
                                                            _export_onnx_opset_version)
        torch._C._jit_pass_dce_allow_deleting_nodes_with_side_effects(graph)

    if _onnx_shape_inference:
        torch._C._jit_pass_onnx_graph_shape_type_inference(graph, params_dict, _export_onnx_opset_version)

    params_dict = torch._C._jit_pass_onnx_eliminate_unused_items(graph, params_dict)

    # For ONNX opset < 9, constants only have three data types: float16, float, double.
    # In this pass transform constants of other data types to float/double + cast operator.
    if _export_onnx_opset_version < 9:
        torch._C._jit_pass_onnx_cast_all_constant_to_floating(graph)

    if verbose:
        print(graph)

    params_dict = torch._C._jit_pass_filter_non_tensor_arguments(params_dict)
    torch._C._jit_decay_packed_param_input_types(graph)

    return graph, params_dict, torch_out
