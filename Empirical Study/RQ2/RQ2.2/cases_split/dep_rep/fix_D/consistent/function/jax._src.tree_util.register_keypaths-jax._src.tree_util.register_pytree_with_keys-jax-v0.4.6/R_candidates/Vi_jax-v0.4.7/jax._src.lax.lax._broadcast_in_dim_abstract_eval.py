def _broadcast_in_dim_abstract_eval(x, *dyn_shape, shape, broadcast_dimensions):
  if dyn_shape: raise NotImplementedError
  assert not any(d is None for d in shape)  # not implemented
  del dyn_shape
  if not any(isinstance(d, core.DArray) and
             type(core.get_aval(d).dtype) is core.bint for d in shape):
    shape = _broadcast_in_dim_shape_rule(  # error checking
        x, shape=shape, broadcast_dimensions=broadcast_dimensions)
    return core.ShapedArray(shape, x.dtype, x.weak_type, x.named_shape)
  # If any BInts in shape, produce a DShapedArray (even if x is a ShapedArray)
  # TODO(mattjj): unify DShapedArray with ShapedArray, and remove this code
  return core.DShapedArray(shape, x.dtype, x.weak_type)
