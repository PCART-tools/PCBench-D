def _parse_entry(arg_name, entry):
  # Dictionaries mapping axis names to positional axes
  if isinstance(entry, dict) and all(isinstance(v, int) for v in entry.keys()):
    result = AxisNamePos(((name, axis) for axis, name in entry.items()),
                         user_repr=str(entry))
    num_mapped_dims = len(entry)
  # Non-empty lists or tuples that optionally terminate with an ellipsis
  elif isinstance(entry, (tuple, list)):
    if entry and entry[-1] == ...:
      constr = AxisNamePos
      entry = entry[:-1]
      tail = [DotDotDotRepr()] if isinstance(entry, list) else (DotDotDotRepr(),)
      user_repr = str(entry + tail)
    else:
      constr = partial(AxisNamePosWithRank, expected_rank=len(entry))
      user_repr = str(entry)
    result = constr(((name, axis) for axis, name in enumerate(entry)
                     if name is not None),
                    user_repr=user_repr)
    num_mapped_dims = sum(name is not None for name in entry)
  else:
    raise TypeError(f"""\
Value mapping specification in xmap {arg_name} pytree can be either:
- lists of axis names (possibly ending with the ellipsis object: ...)
- dictionaries that map positional axes (integers) to axis names (e.g. {{2: 'name'}})
but got: {entry}""")
  if len(result) != num_mapped_dims:
    raise ValueError(f"Named axes should be unique within each {arg_name} argument "
                     f"specification, but one them is: {entry}")
  for axis in result.values():
    if axis < 0:
      raise ValueError(f"xmap doesn't support negative axes in {arg_name}")
  return result
