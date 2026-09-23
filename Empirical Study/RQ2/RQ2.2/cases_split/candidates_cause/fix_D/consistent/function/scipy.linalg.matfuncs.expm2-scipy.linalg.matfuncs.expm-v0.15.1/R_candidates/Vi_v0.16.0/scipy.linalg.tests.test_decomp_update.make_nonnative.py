def make_nonnative(arrs):
    out = []
    for a in arrs:
        out.append(a.astype(a.dtype.newbyteorder()))
    return out
