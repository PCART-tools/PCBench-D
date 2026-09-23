  def __init__(self,
               points,
               values,
               method="linear",
               bounds_error=False,
               fill_value=nan):
    if method not in ("linear", "nearest"):
      raise ValueError(f"method {method!r} is not defined")
    self.method = method
    self.bounds_error = bounds_error
    if self.bounds_error:
      raise NotImplementedError("`bounds_error` takes no effect under JIT")

    check_arraylike("RegularGridInterpolator", values)
    if len(points) > values.ndim:
      ve = f"there are {len(points)} point arrays, but values has {values.ndim} dimensions"
      raise ValueError(ve)

    values, = promote_dtypes_inexact(values)

    if fill_value is not None:
      check_arraylike("RegularGridInterpolator", fill_value)
      fill_value = asarray(fill_value)
      if not can_cast(fill_value.dtype, values.dtype, casting='same_kind'):
        ve = "fill_value must be either 'None' or of a type compatible with values"
        raise ValueError(ve)
    self.fill_value = fill_value

    # TODO: assert sanity of `points` similar to SciPy but in a JIT-able way
    check_arraylike("RegularGridInterpolator", *points)
    self.grid = tuple(asarray(p) for p in points)
    self.values = values
