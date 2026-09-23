def snapshot() -> dict[str, Any]:
    r"""Return a dictionary of MTIA memory allocator history"""

    return torch._C._mtia_memorySnapshot()
