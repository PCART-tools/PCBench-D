@util.implements(np.atleast_1d, update_doc=False, lax_description=_ARRAY_VIEW_DOC)
@jit
def atleast_1d(*arys: ArrayLike) -> Array | list[Array]:
  # TODO(jakevdp): Non-array input deprecated 2023-09-22; change to error.
  util.check_arraylike("atleast_1d", *arys, emit_warning=True)
  if len(arys) == 1:
    return array(arys[0], copy=False, ndmin=1)
  else:
    return [array(arr, copy=False, ndmin=1) for arr in arys]
