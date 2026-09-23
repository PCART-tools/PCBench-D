@_wraps(np.roll)
def roll(a, shift, axis: Optional[Union[int, Sequence[int]]] = None):
  _check_arraylike("roll", a,)
  if isinstance(axis, list):
    axis = tuple(axis)
  return _roll(a, shift, axis)
