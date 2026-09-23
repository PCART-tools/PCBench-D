def _add_arrays(x, y):
  if (isinstance(a := core.get_aval(x), ShapedArray) and
      dtypes.issubdtype(a.dtype, dtypes.extended)):
    return dtype._rules.add(dtype, x, y)  # type: ignore
  return add(x, y)
