def check_device(a: Tensor, b: Tensor) -> bool:
    return a.is_cuda and b.is_cuda
