def all_bdims(*shapes):
  bdims = (itertools.chain([cast(Optional[int], None)],
                           range(len(shape) + 1)) for shape in shapes)
  return (t for t in itertools.product(*bdims) if not all(e is None for e in t))
