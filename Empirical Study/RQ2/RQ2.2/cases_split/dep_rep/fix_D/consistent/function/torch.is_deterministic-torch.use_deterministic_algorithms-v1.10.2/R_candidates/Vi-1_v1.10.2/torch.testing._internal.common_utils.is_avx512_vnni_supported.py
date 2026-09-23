def is_avx512_vnni_supported():
    if sys.platform != 'linux':
        return False
    with open("/proc/cpuinfo", encoding="ascii") as f:
        lines = f.read()
    return "avx512vnni" in lines
