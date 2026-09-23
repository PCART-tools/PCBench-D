@util._wraps(np.flip, lax_description=_ARRAY_VIEW_DOC)
def flip(m: ArrayLike, axis: Optional[Union[int, Tuple[int, ...]]] = None) -> Array:
  util._check_arraylike("flip", m)
  return _flip(asarray(m), reductions._ensure_optional_axes(axis))
