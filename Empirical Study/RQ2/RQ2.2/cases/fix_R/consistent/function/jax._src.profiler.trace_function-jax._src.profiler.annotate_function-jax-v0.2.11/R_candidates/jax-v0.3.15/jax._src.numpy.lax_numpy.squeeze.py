@_wraps(np.squeeze, lax_description=_ARRAY_VIEW_DOC)
def squeeze(a, axis: Optional[Union[int, Tuple[int, ...]]] = None):
  return _squeeze(a, _ensure_index_tuple(axis) if axis is not None else None)
