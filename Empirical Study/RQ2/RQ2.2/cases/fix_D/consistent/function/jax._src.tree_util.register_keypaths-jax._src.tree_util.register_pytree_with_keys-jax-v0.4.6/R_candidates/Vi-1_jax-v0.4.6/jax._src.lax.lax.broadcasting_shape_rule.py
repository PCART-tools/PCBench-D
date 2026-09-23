def broadcasting_shape_rule(name, *avals):
  shapes = [aval.shape for aval in avals if aval.shape]
  if not shapes:
    return ()
  if len({len(shape) for shape in shapes}) != 1:
    msg = '{}: arrays must have same number of dimensions, got {}.'
    raise TypeError(msg.format(name, ', '.join(map(str, map(tuple, shapes)))))
  # TODO(mattjj): de-duplicate with _try_broadcast_shapes
  result_shape = []
  for ds in zip(*shapes):
    if all(core.same_referent(d, ds[0]) for d in ds[1:]):
      # if all axes are identical objects, the resulting size is the object
      result_shape.append(ds[0])
    else:
      # if all dims are equal (or 1), the result is the non-1 size
      non_1s = [d for d in ds if not core.symbolic_equal_dim(d, 1)]
      if not non_1s:
        result_shape.append(1)
      elif all(core.symbolic_equal_dim(non_1s[0], d) for d in non_1s[1:]):
        result_shape.append(non_1s[0])
      else:
        raise TypeError(f'{name} got incompatible shapes for broadcasting: '
                        f'{", ".join(map(str, map(tuple, shapes)))}.')

  return tuple(result_shape)
