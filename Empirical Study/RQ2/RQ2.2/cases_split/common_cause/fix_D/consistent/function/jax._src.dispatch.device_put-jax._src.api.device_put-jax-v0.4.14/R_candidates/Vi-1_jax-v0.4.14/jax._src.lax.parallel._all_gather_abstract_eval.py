def _all_gather_abstract_eval(x, *, all_gather_dimension, axis_name, axis_index_groups, axis_size, tiled):
  if not isinstance(axis_name, (list, tuple)):
    axis_name = (axis_name,)
  x_aval = raise_to_shaped(x)
  new_shape = list(x_aval.shape)
  if tiled:
    new_shape[all_gather_dimension] *= axis_size
  else:
    new_shape.insert(all_gather_dimension, axis_size)
  new_named_shape = {name: size for name, size in x_aval.named_shape.items()
                     if name not in axis_name}
  return x_aval.update(shape=new_shape, named_shape=new_named_shape)
