def _any(predicates: Array) -> Array:
  f = _const(predicates, False)
  predicates_shape = predicates.shape
  all_dimensions = tuple(range(len(predicates_shape)))
  return reduce(predicates, f, bitwise_or, all_dimensions)
