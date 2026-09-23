def lookup_exactly_one_of(d: AxisNamePos, names: Set[AxisName]) -> Optional[int]:
  res = None
  for name in names:
    if name in d:
      if res is not None:
        raise ValueError("An input was mapped to the same resource twice")
      res = d[name]
  return res
