@util._wraps(np.transpose, lax_description=_ARRAY_VIEW_DOC)
def transpose(a: ArrayLike, axes: Optional[Sequence[int]] = None) -> Array:
  util.check_arraylike("transpose", a)
  axes_ = list(range(ndim(a))[::-1]) if axes is None else axes
  axes_ = [_canonicalize_axis(i, ndim(a)) for i in axes_]
  return lax.transpose(a, axes_)
