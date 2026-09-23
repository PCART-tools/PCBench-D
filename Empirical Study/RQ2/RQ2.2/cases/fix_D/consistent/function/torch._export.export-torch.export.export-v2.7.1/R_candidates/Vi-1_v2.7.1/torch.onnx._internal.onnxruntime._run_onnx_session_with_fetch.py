def _run_onnx_session_with_fetch(
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

    inputs = tuple(
        _adjust_scalar_from_fx_to_onnx(arg, value_info)
        for arg, value_info in zip(inputs, input_value_infos)
    )
    feed = {
        name: onnxruntime.OrtValue.ortvalue_from_numpy(tensor.cpu().numpy())
        for name, tensor in zip(input_names, inputs)
    }
    ort_outputs = sess.run(output_names, feed)
    pth_outputs = tuple(
        _adjust_scalar_from_onnx_to_fx(
            torch.from_numpy(value),
            prim_output,
        )
        for value, prim_output in zip(ort_outputs, normalized_prim_outputs)
    )
    return pth_outputs
