@util._wraps(np.atleast_3d, update_doc=False, lax_description=_ARRAY_VIEW_DOC)
@jit
def atleast_3d(*arys: ArrayLike) -> Union[Array, List[Array]]:
  if len(arys) == 1:
    arr = asarray(arys[0])
    if ndim(arr) == 0:
      arr = expand_dims(arr, axis=(0, 1, 2))
    elif ndim(arr) == 1:
      arr = expand_dims(arr, axis=(0, 2))
    elif ndim(arr) == 2:
      arr = expand_dims(arr, axis=2)
    return arr
  else:
    return [atleast_3d(arr) for arr in arys]
