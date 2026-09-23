def _iota_padding_rule(in_avals, out_avals, *dyn_shape, dtype, shape, dimension):
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
  return [iota_p.bind(*new_dyn_shape, shape=tuple(new_shape),
                      dtype=dtype, dimension=dimension)]
