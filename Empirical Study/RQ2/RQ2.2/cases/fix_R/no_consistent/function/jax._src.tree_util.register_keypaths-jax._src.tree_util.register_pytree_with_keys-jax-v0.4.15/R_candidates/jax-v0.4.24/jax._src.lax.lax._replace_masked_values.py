def _replace_masked_values(x, val, padded_axes):
  if not padded_axes: return x
  dtype = dtypes._scalar_type_to_dtype(int)
  masks = [broadcasted_iota(dtype, x.shape, i) < d for i, d in padded_axes]
  return select(_reduce(operator.and_, masks), x, full_like(x, val))
