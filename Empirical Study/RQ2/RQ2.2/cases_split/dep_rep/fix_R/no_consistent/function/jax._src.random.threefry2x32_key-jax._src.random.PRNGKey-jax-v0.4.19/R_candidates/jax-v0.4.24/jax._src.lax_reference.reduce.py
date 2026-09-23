def reduce(operand, init_value, computation, dimensions):  # pylint: disable=redefined-builtin
  reducer = _make_reducer(computation, init_value)
  return reducer(operand, tuple(dimensions)).astype(np.asarray(operand).dtype)
