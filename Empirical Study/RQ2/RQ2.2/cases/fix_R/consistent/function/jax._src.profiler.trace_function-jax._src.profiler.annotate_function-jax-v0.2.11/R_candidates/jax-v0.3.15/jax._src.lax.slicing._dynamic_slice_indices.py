def _dynamic_slice_indices(operand, start_indices: Any):
  # Normalize the start_indices w.r.t. operand.shape
  if len(start_indices) != operand.ndim:
    msg = ("Length of slice indices must match number of operand dimensions ({} "
          "vs {})")
    raise ValueError(msg.format(len(start_indices), operand.shape))
  if not isinstance(start_indices, (tuple, list)):
    if start_indices.ndim != 1:
      raise ValueError("Slice indices must be a 1D sequence, got {}"
                       .format(start_indices.shape))
    start_indices = [i for i in start_indices]
  return [np.asarray(i + d if i < 0 else i, lax._dtype(i))
          if isinstance(i, (int, np.integer)) and core.is_constant_dim(d)
          else lax.select(
              lax.lt(i, lax._const(i, 0)),
              lax.add(i, lax.convert_element_type(core.dimension_as_value(d), lax._dtype(i))),
              i)
          for i, d in zip(start_indices, operand.shape)]
