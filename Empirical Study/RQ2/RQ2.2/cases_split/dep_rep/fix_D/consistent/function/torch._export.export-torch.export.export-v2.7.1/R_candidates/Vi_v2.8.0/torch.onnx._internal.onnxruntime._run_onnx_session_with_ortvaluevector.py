def _run_onnx_session_with_ortvaluevector(
    sess: "onnxruntime.InferenceSession",
    input_names: tuple[str, ...],
    inputs: tuple[torch.Tensor, ...],
    input_devices: tuple["ORTC.OrtDevice", ...],
    output_names: tuple[str, ...],
    outputs: tuple[torch.Tensor, ...],
    output_devices: tuple["ORTC.OrtDevice", ...],
    preallocate_output: bool,
    input_value_infos: tuple["onnx.ValueInfoProto", ...],  # type: ignore[name-defined]
    normalized_prim_outputs: tuple[
        Union[
            torch.Tensor, torch.SymInt, int, torch.SymFloat, float, torch.SymBool, bool
        ],
        ...,
    ],
) -> tuple[Union[torch.Tensor, int, float, bool], ...]:
    import onnxruntime
    from onnxruntime.capi import _pybind_state as ORTC

    _nvtx_range_push("contiguous")
    inputs = tuple(
        _adjust_scalar_from_fx_to_onnx(arg, value_info)
        for arg, value_info in zip(inputs, input_value_infos)
    )
    _nvtx_range_pop()

    _nvtx_range_push("push_back_batch")
    ort_inputs = _get_ortvalues_from_torch_tensors(inputs, input_devices)

    # preallocate output pytorch Tensors and use the buffers affined to the torch device for the output ortvalue.
    # Because the output ortvalue is not allocated and owned by ort, it does not need to convert the output ortvalue
    # to torch Tensor transferring the ownership.
    if preallocate_output:
        pth_outputs = tuple(
            _to_real_tensor(t) if isinstance(t, FakeTensor) else t for t in outputs
        )
        ort_outputs = _get_ortvalues_from_torch_tensors(pth_outputs, output_devices)
    else:
        ort_outputs = ORTC.OrtValueVector()
    _nvtx_range_pop()

    _nvtx_range_push("run_with_ortvaluevector")
    run_options = onnxruntime.RunOptions()
    run_options.add_run_config_entry("disable_synchronize_execution_providers", "1")
    sess.run_with_ortvaluevector(
        run_options, input_names, ort_inputs, output_names, ort_outputs, output_devices
    )
    _nvtx_range_pop()

    # Post-processing step:
    #  wrap ORT's outputs to the schema represented by
    #  `prim_output` (obtained by running the original
    #  torch.fx.GraphModule).
    if preallocate_output:
        # Profile the ORT-to-PyTorch type cast below
        _nvtx_range_push("after run_with_ortvaluevector")
        # Outputs are stored on pre-allocated torch.Tensors' memory,
        # so this case doesn't need to convert ORTValue to torch.Tensor.
        pth_outputs = tuple(
            _adjust_scalar_from_onnx_to_fx(onnx_output, prim_output)  # type: ignore[misc]
            for onnx_output, prim_output in zip(pth_outputs, normalized_prim_outputs)
        )
        _nvtx_range_pop()
        return pth_outputs
    else:
        import onnxruntime.training

        # Profile the two ORT-to-PyTorch type casts below
        _nvtx_range_push("after run_with_ortvaluevector")
        # Map ORTValue to torch.Tensor.
        pth_outputs = onnxruntime.training.ortmodule._utils._ortvalues_to_torch_tensor(
            ort_outputs
        )
        # Change some torch.Tensor to int, float, bool.
        pth_outputs = tuple(
            _adjust_scalar_from_onnx_to_fx(onnx_output, prim_output)  # type: ignore[misc]
            for onnx_output, prim_output in zip(pth_outputs, normalized_prim_outputs)
        )
        _nvtx_range_pop()
        return pth_outputs
