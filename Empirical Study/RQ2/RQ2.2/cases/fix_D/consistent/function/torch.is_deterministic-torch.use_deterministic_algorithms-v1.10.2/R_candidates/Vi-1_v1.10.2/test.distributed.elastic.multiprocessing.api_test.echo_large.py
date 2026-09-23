def echo_large(size: int) -> Dict[int, str]:
    """
    returns a large output ({0: test0", 1: "test1", ..., (size-1):f"test{size-1}"})
    """
    out = {}
    for idx in range(0, size):
        out[idx] = f"test{idx}"
    return out
