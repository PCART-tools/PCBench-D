@implements(np.sum, skip_params=['out'], extra_params=_PROMOTE_INTEGERS_DOC)
def sum(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
        out: None = None, keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None, promote_integers: bool = True) -> Array:
  return _reduce_sum(a, axis=_ensure_optional_axes(axis), dtype=dtype, out=out,
                     keepdims=keepdims, initial=initial, where=where,
                     promote_integers=promote_integers)
