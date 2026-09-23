def check_error(res: int) -> None:
    if res != _cudart.cudaError.success:
        raise CudaError(res)
