def _broadcast_in_dim_padding_rule(in_avals, out_avals, x, *dyn_shape,
                                   shape, broadcast_dimensions):
  del in_avals, dyn_shape
  out_aval, = out_avals
  new_shape = []
  new_dyn_shape = []
  for d in out_aval.shape:
    if type(d) is pe.BoundedAxisSize:
      new_shape.append(d.bound)
    elif type(d) is int:
      new_shape.append(d)
    else:
      assert isinstance(d, core.Tracer)
      new_shape.append(None)
      new_dyn_shape.append(d)
  return [broadcast_in_dim_p.bind(x, *new_dyn_shape, shape=tuple(new_shape),
                                  broadcast_dimensions=broadcast_dimensions)]
