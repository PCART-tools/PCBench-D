def _split_on_axis(op, axis):
  @_wraps(getattr(np, op), update_doc=False)
  def f(ary, indices_or_sections):
    return _split(op, ary, indices_or_sections, axis=axis)
  return f
