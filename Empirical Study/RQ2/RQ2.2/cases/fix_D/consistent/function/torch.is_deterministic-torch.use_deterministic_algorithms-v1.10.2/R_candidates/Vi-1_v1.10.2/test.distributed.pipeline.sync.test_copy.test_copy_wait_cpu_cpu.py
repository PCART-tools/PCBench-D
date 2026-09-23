def test_copy_wait_cpu_cpu():
    prev_stream = CPUStream
    next_stream = CPUStream
    _test_copy_wait(prev_stream, next_stream)
