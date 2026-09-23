def _reshape_masking_rule(padded_args, logical_shapes, polymorphic_shapes,
                          new_sizes, dimensions):
  operand, = padded_args
  old_shape, = polymorphic_shapes
  def is_poly(size): return type(size) is masking.Poly and not size.is_constant
  def merge_const_sizes(shape):
    """Merges all nonpolymorphic sizes into the previous polymorphic size."""
    poly_dims = [i for i, size in enumerate(shape) if is_poly(size)]
    return [prod(shape[start:stop])
            for start, stop in zip([0] + poly_dims, poly_dims + [len(shape)])]
  if merge_const_sizes(old_shape) != merge_const_sizes(new_sizes):
    raise NotImplementedError(
      "Reshape on padded dimensions causing fragmentation is not supported.")

  return reshape(operand,
                 new_sizes=masking.padded_shape_as_value(new_sizes),
                 dimensions=dimensions)
