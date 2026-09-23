@contextlib.contextmanager
def use_mem_pool(pool: MemPool, device: Union[Device, int] = None):
    r"""A context manager that routes allocations to a given pool.

    Args:
        pool(torch.cuda.MemPool): a MemPool object to be made active so that
            allocations route to this pool.
        device (torch.device or int, optional): selected device. Uses MemPool on
            the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    """
    ctx = MemPoolContext(pool)
    device_index = (
        torch.cuda.current_device() if device is None else _get_device_index(device)
    )
    _cuda_beginAllocateToPool(device_index, pool.id)
    try:
        yield
    finally:
        _cuda_endAllocateCurrentStreamToPool(device_index, pool.id)
        _cuda_releasePool(device_index, pool.id)
        del ctx
