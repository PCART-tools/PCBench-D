def rev(operand, dimensions):
  dimensions = frozenset(dimensions)
  indexer = (_slice(None, None, -1) if d in dimensions else _slice(None)
             for d in range(np.ndim(operand)))
  return operand[tuple(indexer)]
