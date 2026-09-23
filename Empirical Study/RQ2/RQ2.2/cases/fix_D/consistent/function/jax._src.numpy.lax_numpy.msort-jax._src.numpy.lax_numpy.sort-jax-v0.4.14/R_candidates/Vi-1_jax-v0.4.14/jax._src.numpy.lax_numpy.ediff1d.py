@util._wraps(np.ediff1d, lax_description=_EDIFF1D_DOC)
@jit
def ediff1d(ary: ArrayLike, to_end: Optional[ArrayLike] = None,
            to_begin: Optional[ArrayLike] = None) -> Array:
  util.check_arraylike("ediff1d", ary)
  arr = ravel(ary)
  result = lax.sub(arr[1:], arr[:-1])
  if to_begin is not None:
    util.check_arraylike("ediff1d", to_begin)
    result = concatenate((ravel(asarray(to_begin, dtype=arr.dtype)), result))
  if to_end is not None:
    util.check_arraylike("ediff1d", to_end)
    result = concatenate((result, ravel(asarray(to_end, dtype=arr.dtype))))
  return result
