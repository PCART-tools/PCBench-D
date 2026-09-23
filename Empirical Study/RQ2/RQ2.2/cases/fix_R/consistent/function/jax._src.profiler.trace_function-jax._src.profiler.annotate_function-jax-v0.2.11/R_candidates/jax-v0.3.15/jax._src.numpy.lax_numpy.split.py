@_wraps(np.split, lax_description=_ARRAY_VIEW_DOC)
def split(ary, indices_or_sections, axis: int = 0):
  return _split("split", ary, indices_or_sections, axis=axis)
