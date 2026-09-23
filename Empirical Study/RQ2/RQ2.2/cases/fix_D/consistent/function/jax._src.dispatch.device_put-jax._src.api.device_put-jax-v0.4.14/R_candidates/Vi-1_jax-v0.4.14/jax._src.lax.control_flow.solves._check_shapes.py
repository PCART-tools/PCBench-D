def _check_shapes(func_name, expected_name, actual, expected):
  actual_shapes = _map(np.shape, tree_leaves(actual))
  expected_shapes = _map(np.shape, tree_leaves(expected))
  if actual_shapes != expected_shapes:
    raise ValueError(
        f"{func_name}() output shapes must match {expected_name}, "
        f"got {actual_shapes} and {expected_shapes}")
