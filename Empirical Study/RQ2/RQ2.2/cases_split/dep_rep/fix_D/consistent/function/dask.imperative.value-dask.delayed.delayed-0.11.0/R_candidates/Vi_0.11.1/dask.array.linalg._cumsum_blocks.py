def _cumsum_blocks(it):
    total = 0
    for x in it:
        total_previous = total
        total += x
        yield (total_previous, total)
