def _Tensor_to_torch(tensor):
    """
    PyTorch tensor interop (TensorCPU methods)

    Can be accessed as:
      workspace.Workspace.current.blobs['foo'].tensor().to_torch()
    """
    # avoiding circular dependency
    import torch
    handle = tensor._tensor_impl_raw_handle()
    return torch._C._wrap_tensor_impl(handle)
