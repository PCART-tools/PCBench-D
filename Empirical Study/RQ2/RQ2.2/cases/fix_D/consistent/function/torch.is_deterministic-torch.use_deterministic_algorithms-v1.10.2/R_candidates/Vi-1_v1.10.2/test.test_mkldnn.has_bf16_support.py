@functools.lru_cache(maxsize=None)
def has_bf16_support():
    import sys
    if sys.platform != 'linux':
        return False
    with open("/proc/cpuinfo", encoding="ascii") as f:
        lines = f.read()
    return all(word in lines for word in ["avx512bw", "avx512vl", "avx512dq"])
