@dec.slow
@dec.skipif(np.dtype(np.intp).itemsize < 8, "test only on 64-bit, else too slow")
def test_orth_memory_efficiency():
    # Pick n so that 16*n bytes is reasonable but 8*n*n bytes is unreasonable.
    # Keep in mind that @dec.slow tests are likely to be running
    # under configurations that support 4Gb+ memory for tests related to
    # 32 bit overflow.
    n = 10*1000*1000
    try:
        _check_orth(n)
    except MemoryError:
        raise AssertionError('memory error perhaps caused by orth regression')
