def _broadcast_in_dim_transpose_rule(ct, operand, *dyn_shape,
                                     shape, broadcast_dimensions):
  if type(ct) is ad_util.Zero:
    return [ad_util.Zero(operand.aval)]
  unit_dims = [i for i, s in enumerate(operand.aval.shape)
               if core.definitely_equal(s, 1)]
  bdims = tuple(np.delete(broadcast_dimensions, unit_dims))
  axes = tuple(np.delete(range(len(shape)), bdims))
  return ([expand_dims(_reduce_sum(ct, axes), unit_dims)] +
          [None] * len(dyn_shape))
