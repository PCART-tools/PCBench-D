def _tensor_nbytes(numel: int, dtype) -> int:
    return numel * dtype.itemsize
