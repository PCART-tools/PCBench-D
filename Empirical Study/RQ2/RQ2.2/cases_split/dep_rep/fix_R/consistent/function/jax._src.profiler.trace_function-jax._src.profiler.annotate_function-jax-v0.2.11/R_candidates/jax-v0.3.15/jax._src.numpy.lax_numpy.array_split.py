@_wraps(np.array_split)
def array_split(ary, indices_or_sections, axis: int = 0):
  return _split("array_split", ary, indices_or_sections, axis=axis)
