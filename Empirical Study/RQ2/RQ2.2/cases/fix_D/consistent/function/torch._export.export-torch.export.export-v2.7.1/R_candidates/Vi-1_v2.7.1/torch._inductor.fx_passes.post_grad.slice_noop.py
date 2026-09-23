@register_noop_decomp(aten.slice)
def slice_noop(self, dim=0, start=None, end=None, step=1):
    if start is None or end is None:
        return False
    if (
        statically_known_true(sym_eq(start, 0))
        and statically_known_true(end >= 2**63 - 1)
        and statically_known_true(sym_eq(step, 1))
    ):
        return True
    return False
