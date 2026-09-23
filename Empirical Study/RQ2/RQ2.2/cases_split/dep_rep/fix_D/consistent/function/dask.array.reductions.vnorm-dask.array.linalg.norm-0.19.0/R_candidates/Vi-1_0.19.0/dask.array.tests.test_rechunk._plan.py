def _plan(old_chunks, new_chunks, itemsize=1, block_size_limit=1e7):
    return plan_rechunk(old_chunks, new_chunks,
                        itemsize=itemsize,
                        block_size_limit=block_size_limit)
