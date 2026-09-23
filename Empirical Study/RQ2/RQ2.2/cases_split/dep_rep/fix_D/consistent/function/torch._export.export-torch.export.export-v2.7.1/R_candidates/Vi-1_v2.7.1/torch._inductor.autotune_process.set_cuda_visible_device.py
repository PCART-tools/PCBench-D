@contextlib.contextmanager
def set_cuda_visible_device(device: Optional[int]):
    """
    Context manager to set the CUDA_VISIBLE_DEVICES environment variable to the
    specified single device. If device is None, don't manipulate the environment.
    """
    if device is None:
        yield
        return

    current = os.environ.get(CUDA_VISIBLE_DEVICES)
    os.environ[CUDA_VISIBLE_DEVICES] = str(device)
    try:
        yield
    finally:
        if current is None:
            del os.environ[CUDA_VISIBLE_DEVICES]
        else:
            os.environ[CUDA_VISIBLE_DEVICES] = current
