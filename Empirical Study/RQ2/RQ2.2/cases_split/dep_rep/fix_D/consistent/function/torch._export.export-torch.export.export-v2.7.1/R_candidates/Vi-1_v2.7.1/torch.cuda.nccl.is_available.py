def is_available(tensors):
    if not hasattr(torch._C, "_nccl_all_reduce"):
        warnings.warn("PyTorch is not compiled with NCCL support")
        return False

    devices = set()
    for tensor in tensors:
        if tensor.is_sparse:
            return False
        if not tensor.is_contiguous():
            return False
        if not tensor.is_cuda:
            return False
        device = tensor.get_device()
        if device in devices:
            return False
        devices.add(device)

    return True
