def _get_ortvalues_from_torch_tensors(
    tensors: tuple[torch.Tensor, ...], devices: tuple["ORTC.OrtDevice", ...]
) -> tuple[torch.Tensor, ...]:
    from onnxruntime.capi import _pybind_state as ORTC

    from torch.onnx._internal.fx.type_utils import _TORCH_DTYPE_TO_NUMPY_DTYPE

    ortvalues = ORTC.OrtValueVector()
    ortvalues.reserve(len(tensors))
    dtypes = []
    shapes = []
    data_ptrs = []

    for tensor in tensors:
        dtypes.append(_TORCH_DTYPE_TO_NUMPY_DTYPE[tensor.dtype])
        shapes.append(tensor.size())
        data_ptrs.append(tensor.data_ptr())
    ortvalues.push_back_batch(tensors, data_ptrs, dtypes, shapes, devices)
    return ortvalues
