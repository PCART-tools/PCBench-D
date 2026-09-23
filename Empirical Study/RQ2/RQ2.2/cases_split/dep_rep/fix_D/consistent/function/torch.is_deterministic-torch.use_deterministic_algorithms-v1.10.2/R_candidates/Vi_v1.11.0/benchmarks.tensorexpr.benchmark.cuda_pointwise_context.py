@contextlib.contextmanager
def cuda_pointwise_context(loop_levels, block_count, block_size):
    if loop_levels:
        old_loop_levels = torch._C._jit_get_te_cuda_pointwise_loop_levels()
        torch._C._jit_set_te_cuda_pointwise_loop_levels(loop_levels)
    if block_count:
        old_block_count = torch._C._jit_get_te_cuda_pointwise_block_count()
        torch._C._jit_set_te_cuda_pointwise_block_count(block_count)
    if block_size:
        old_block_size = torch._C._jit_get_te_cuda_pointwise_block_size()
        torch._C._jit_set_te_cuda_pointwise_block_size(block_size)

    yield

    if loop_levels:
        torch._C._jit_set_te_cuda_pointwise_loop_levels(old_loop_levels)
    if block_count:
        torch._C._jit_set_te_cuda_pointwise_block_count(old_block_count)
    if block_size:
        torch._C._jit_set_te_cuda_pointwise_block_size(old_block_size)
