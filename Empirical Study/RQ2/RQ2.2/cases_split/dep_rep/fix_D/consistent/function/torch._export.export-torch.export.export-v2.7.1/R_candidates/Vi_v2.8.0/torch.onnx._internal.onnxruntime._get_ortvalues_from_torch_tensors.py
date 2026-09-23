def _get_ortvalues_from_torch_tensors(
    tensors: tuple[torch.Tensor, ...], devices: tuple["ORTC.OrtDevice", ...]
) -> tuple[torch.Tensor, ...]:
    # TODO(justinchuby): Refactor this function
    import numpy as np
    from onnxruntime.capi import _pybind_state as ORTC

    torch_dtype_to_numpy_dtype = {
        torch.float16: np.float16,
        torch.float32: np.float32,
        torch.float64: np.float64,
        torch.uint8: np.uint8,
        torch.int8: np.int8,
        torch.int16: np.int16,
        torch.int32: np.int32,
        torch.int64: np.longlong,
        torch.bool: np.bool_,
    }
    ortvalues = ORTC.OrtValueVector()
    ortvalues.reserve(len(tensors))
    dtypes = []
    shapes = []
    data_ptrs = []

    for tensor in tensors:
        dtypes.append(torch_dtype_to_numpy_dtype[tensor.dtype])
        shapes.append(tensor.size())
        data_ptrs.append(tensor.data_ptr())
    ortvalues.push_back_batch(tensors, data_ptrs, dtypes, shapes, devices)
    return ortvalues
