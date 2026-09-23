def _get_current_allocator() -> _CUDAAllocator:
    r"""Return the allocator being currently used.

    .. note::
        See :ref:`cuda-memory-management` for details on creating and using a custom allocator
    """
    return _CUDAAllocator(torch._C._cuda_getAllocator())
