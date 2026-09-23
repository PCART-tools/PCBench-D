def _dynamic_slice_indices(
    operand: Array | np.ndarray,
    start_indices: Array | np.ndarray | Sequence[ArrayLike]
  ) -> list[ArrayLike]:
  # Normalize the start_indices w.r.t. operand.shape
  if len(start_indices) != operand.ndim:
    msg = ("Length of slice indices must match number of operand dimensions ({} "
          "vs {})")
    raise ValueError(msg.format(len(start_indices), operand.shape))
  if not isinstance(start_indices, (tuple, list)):
    if start_indices.ndim != 1:  # type: ignore[union-attr]
      raise ValueError("Slice indices must be a 1D sequence, got {}"
                       .format(start_indices.shape))  # type: ignore[union-attr]
    start_indices = list(start_indices)
  result: list[ArrayLike] = []
  # Loop to correct for negative indices.
  for i, d in zip(start_indices, operand.shape):
    # If i is unsigned, then it cannot be negative.
    if dtypes.issubdtype(_dtype(i), np.unsignedinteger):
      result.append(i)
      continue
    # Test whether i and d are static to avoid unnecessary staging.
    if isinstance(i, (int, np.integer)) and core.is_constant_dim(d):
      result.append(lax.convert_element_type(i + d if i < 0 else i, _dtype(i)))
      continue
    d = core.dimension_as_value(d)
    if isinstance(i, (int, np.integer)):
      result.append(i + lax.convert_element_type(d, _dtype(i)) if i < 0 else i)
      continue
    d_arr = lax.convert_element_type(d, _dtype(i))
    result.append(lax.select(i < 0, i + d_arr, i))
  return result
