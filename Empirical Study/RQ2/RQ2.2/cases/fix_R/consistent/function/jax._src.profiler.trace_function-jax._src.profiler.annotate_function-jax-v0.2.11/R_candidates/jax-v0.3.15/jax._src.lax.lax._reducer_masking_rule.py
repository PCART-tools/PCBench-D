def _reducer_masking_rule(prim, identity, padded_vals, logical_shapes,
                          axes, input_shape=None, **reduce_kwargs):
  (padded_val,), (logical_shape,) = padded_vals, logical_shapes
  padded_shape = masking.padded_shape_as_value(padded_val.shape)
  masks = [broadcasted_iota(_dtype(d), padded_shape, i) < d
           for i, d in enumerate(logical_shape) if i in axes]
  mask = _reduce(operator.and_, masks)
  masked_val = select(mask, padded_val, identity(padded_shape, padded_val.dtype))
  prim_bind = partial(prim.bind, **reduce_kwargs)
  bind = prim_bind if input_shape is None else partial(prim_bind, input_shape=padded_shape)
  return bind(masked_val, axes=axes)
