def unzip3(xyzs: Iterable[Tuple[T1, T2, T3]]
    ) -> Tuple[Tuple[T1, ...], Tuple[T2, ...], Tuple[T3, ...]]:
  """Unzip sequence of length-3 tuples into three tuples."""
  # Note: we deliberately don't use zip(*xyzs) because it is lazily evaluated,
  # is too permissive about inputs, and does not guarantee a length-3 output.
  xs: List[T1] = []
  ys: List[T2] = []
  zs: List[T3] = []
  for x, y, z in xyzs:
    xs.append(x)
    ys.append(y)
    zs.append(z)
  return tuple(xs), tuple(ys), tuple(zs)
