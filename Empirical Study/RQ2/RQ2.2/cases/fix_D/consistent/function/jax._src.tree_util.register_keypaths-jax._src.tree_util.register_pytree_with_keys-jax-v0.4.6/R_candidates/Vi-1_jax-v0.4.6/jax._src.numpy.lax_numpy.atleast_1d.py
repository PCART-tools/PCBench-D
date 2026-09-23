@util._wraps(np.atleast_1d, update_doc=False, lax_description=_ARRAY_VIEW_DOC)
@jit
def atleast_1d(*arys: ArrayLike) -> Union[Array, List[Array]]:
  if len(arys) == 1:
    arr = asarray(arys[0])
    return arr if ndim(arr) >= 1 else reshape(arr, -1)
  else:
    return [atleast_1d(arr) for arr in arys]
