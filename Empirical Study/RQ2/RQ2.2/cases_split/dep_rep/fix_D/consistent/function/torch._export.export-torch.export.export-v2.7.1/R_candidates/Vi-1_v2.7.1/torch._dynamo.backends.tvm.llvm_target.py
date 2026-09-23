@functools.lru_cache(None)
def llvm_target():
    if sys.platform == "linux":
        cpuinfo = open("/proc/cpuinfo").read()
        if "avx512" in cpuinfo:
            return "llvm -mcpu=skylake-avx512"
        elif "avx2" in cpuinfo:
            return "llvm -mcpu=core-avx2"
    return "llvm"
