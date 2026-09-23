@SymbolicGridFn
def bmm_grid(b, m, n, meta, *, cdiv):
    return (cdiv(m, meta["BLOCK_M"]) * cdiv(n, meta["BLOCK_N"]), b, 1)
