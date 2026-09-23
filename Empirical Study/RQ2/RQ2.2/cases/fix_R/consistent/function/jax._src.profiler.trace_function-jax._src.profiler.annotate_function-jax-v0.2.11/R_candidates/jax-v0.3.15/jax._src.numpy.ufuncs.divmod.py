@_wraps(np.divmod, module='numpy')
@jit
def divmod(x1, x2):
  x1, x2 = _promote_args("divmod", x1, x2)
  if dtypes.issubdtype(dtypes.dtype(x1), np.integer):
    return floor_divide(x1, x2), remainder(x1, x2)
  else:
    return _float_divmod(x1, x2)
