@util._wraps(np.atleast_2d, update_doc=False, lax_description=_ARRAY_VIEW_DOC)
@jit
def atleast_2d(*arys: ArrayLike) -> Union[Array, List[Array]]:
  if len(arys) == 1:
    arr = asarray(arys[0])
    if ndim(arr) >= 2:
      return arr
    elif ndim(arr) == 1:
      return expand_dims(arr, axis=0)
    else:
      return expand_dims(arr, axis=(0, 1))
  else:
    return [atleast_2d(arr) for arr in arys]
