@util.implements(np.atleast_3d, update_doc=False, lax_description=_ARRAY_VIEW_DOC)
@jit
def atleast_3d(*arys: ArrayLike) -> Array | list[Array]:
  # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
  util.check_arraylike("atleast_3d", *arys, emit_warning=True)
  if len(arys) == 1:
    arr = asarray(arys[0])
    if arr.ndim == 0:
      arr = lax.expand_dims(arr, dimensions=(0, 1, 2))
    elif arr.ndim == 1:
      arr = lax.expand_dims(arr, dimensions=(0, 2))
    elif arr.ndim == 2:
      arr = lax.expand_dims(arr, dimensions=(2,))
    return arr
  else:
    return [atleast_3d(arr) for arr in arys]
