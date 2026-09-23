def is_nvshmem_available() -> bool:
    r"""
    is_nvshmem_available() -> bool

    Check if NVSHMEM is available in current build and on current system.
    """
    try:
        from torch._C._distributed_c10d import _is_nvshmem_available
    except ImportError:
        # Not all builds have NVSHMEM support.
        return False

    # Check if NVSHMEM is available on current system.
    return _is_nvshmem_available()
