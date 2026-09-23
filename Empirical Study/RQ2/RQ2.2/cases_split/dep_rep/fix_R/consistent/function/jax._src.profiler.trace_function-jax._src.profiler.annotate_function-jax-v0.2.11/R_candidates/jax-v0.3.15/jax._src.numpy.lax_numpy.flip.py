@_wraps(np.flip, lax_description=_ARRAY_VIEW_DOC)
def flip(m, axis: Optional[Union[int, Tuple[int, ...]]] = None):
  return _flip(m, _ensure_optional_axes(axis))
