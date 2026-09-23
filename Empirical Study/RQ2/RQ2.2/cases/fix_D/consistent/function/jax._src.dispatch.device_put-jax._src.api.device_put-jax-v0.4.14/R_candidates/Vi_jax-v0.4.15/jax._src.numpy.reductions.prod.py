@_wraps(np.prod, skip_params=['out'], extra_params=_PROMOTE_INTEGERS_DOC)
def prod(a: ArrayLike, axis: Axis = None, dtype: DTypeLike = None,
         out: None = None, keepdims: bool = False,
         initial: Optional[ArrayLike] = None, where: Optional[ArrayLike] = None,
         promote_integers: bool = True) -> Array:
  return _reduce_prod(a, axis=_ensure_optional_axes(axis), dtype=dtype,
                      out=out, keepdims=keepdims, initial=initial, where=where,
                      promote_integers=promote_integers)
