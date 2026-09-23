@skip_if_no_cuda
def test_copy_wait_cpu_cuda(cuda_sleep):
    prev_stream = CPUStream
    next_stream = current_stream(torch.device("cuda"))
    _test_copy_wait(prev_stream, next_stream, cuda_sleep)
