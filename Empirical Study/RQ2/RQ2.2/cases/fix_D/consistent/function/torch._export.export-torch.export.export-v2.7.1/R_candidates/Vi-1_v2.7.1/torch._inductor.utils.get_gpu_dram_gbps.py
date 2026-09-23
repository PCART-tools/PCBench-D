@functools.lru_cache(None)
def get_gpu_dram_gbps() -> int:
    from triton.testing import get_dram_gbps

    return get_dram_gbps()
