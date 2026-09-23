def get_cur_mem(rank, result, prefix):
    """Collect memory allocated values in a result dict in MB"""
    result[prefix] = round(torch.cuda.memory_allocated() / 1024 / 1024)
