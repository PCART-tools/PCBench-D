@skip_if_no_cuda
def test_copy_wait_cuda_cpu(cuda_sleep):
    prev_stream = current_stream(torch.device("cuda"))
    next_stream = CPUStream
    _test_copy_wait(prev_stream, next_stream, cuda_sleep)
