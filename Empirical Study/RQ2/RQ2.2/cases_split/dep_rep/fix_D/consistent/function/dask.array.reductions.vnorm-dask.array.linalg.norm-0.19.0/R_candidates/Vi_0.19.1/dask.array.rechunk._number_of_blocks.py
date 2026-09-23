def _number_of_blocks(chunks):
    return reduce(mul, map(len, chunks))
