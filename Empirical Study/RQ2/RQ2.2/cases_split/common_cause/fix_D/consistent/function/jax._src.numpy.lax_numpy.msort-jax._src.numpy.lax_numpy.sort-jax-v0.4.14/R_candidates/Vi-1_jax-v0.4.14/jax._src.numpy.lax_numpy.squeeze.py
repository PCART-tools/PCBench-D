@util._wraps(np.squeeze, lax_description=_ARRAY_VIEW_DOC)
def squeeze(a: ArrayLike, axis: Optional[Union[int, tuple[int, ...]]] = None) -> Array:
  util.check_arraylike("squeeze", a)
  return _squeeze(asarray(a), _ensure_index_tuple(axis) if axis is not None else None)
