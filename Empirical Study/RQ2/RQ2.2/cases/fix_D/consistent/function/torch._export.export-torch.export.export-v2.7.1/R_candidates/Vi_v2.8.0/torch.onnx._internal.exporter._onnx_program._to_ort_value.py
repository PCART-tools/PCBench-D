def _to_ort_value(tensor: torch.Tensor) -> ort.OrtValue:
    """Convert a PyTorch tensor to an ONNX Runtime OrtValue."""
    import onnxruntime as ort

    from torch.onnx._internal.exporter import _core

    if tensor.dtype == torch.bfloat16 or tensor.dtype in _NP_UNSUPPORTED_DTYPES_8BIT:
        if hasattr(ort.OrtValue, "ortvalue_from_numpy_with_onnx_type"):
            # This requires ONNX Runtime 1.21 or newer
            if tensor.dtype == torch.bfloat16:
                uint_type = torch.uint16
            else:
                uint_type = torch.uint8
            onnx_type = _core.torch_dtype_to_onnx_dtype(tensor.dtype)
            # Make tensor contiguous to ensure view() works
            tensor = tensor.contiguous()
            return ort.OrtValue.ortvalue_from_numpy_with_onnx_type(
                tensor.view(uint_type).numpy(force=True), onnx_element_type=onnx_type
            )
        raise RuntimeError(
            f"Failed to convert tensor of type '{tensor.dtype}' to OrtValue. "
            "Please ensure that ONNX Runtime is built with DLPack support or is the latest version"
        )
    # TODO(#151064): Use dlpack when ORT properly supports it
    return ort.OrtValue.ortvalue_from_numpy(tensor.numpy(force=True))
