def dimension_as_value(d: DimSize):
  """Turns a dimension size into a JAX value that we can compute with.
     This is the identity function for constant dimensions.

     Has the same abstract value as Python constants.
     """
  if isinstance(d, (int, Tracer, np.int32, np.int64)): return d
  # For shape_poly._DimPolynomial
  if hasattr(d, "dimension_as_value"): return d.dimension_as_value()
  return operator.index(d)
