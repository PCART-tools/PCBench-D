@wraps(np.piecewise)
def piecewise(x, condlist, funclist, *args, **kw):
    return map_blocks(
        _int_piecewise,
        x, *condlist,
        dtype=x.dtype,
        name="piecewise",
        funclist=funclist, func_args=args, func_kw=kw
    )
