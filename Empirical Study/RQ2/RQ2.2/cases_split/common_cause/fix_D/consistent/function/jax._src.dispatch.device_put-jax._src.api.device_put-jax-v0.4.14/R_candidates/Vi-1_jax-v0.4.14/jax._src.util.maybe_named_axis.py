def maybe_named_axis(axis, if_pos, if_named):
  try:
    pos = operator.index(axis)
    named = False
  except TypeError:
    named = True
  return if_named(axis) if named else if_pos(pos)
