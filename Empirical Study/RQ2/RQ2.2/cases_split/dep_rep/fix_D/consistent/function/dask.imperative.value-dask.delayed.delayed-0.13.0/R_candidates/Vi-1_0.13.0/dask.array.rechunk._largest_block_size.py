def _largest_block_size(chunks):
    return reduce(mul, map(max, chunks))
