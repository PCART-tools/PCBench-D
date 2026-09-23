def batch_jaxpr(closed_jaxpr, axis_size, in_batched, instantiate, axis_name,
                spmd_axis_name, main_type):
  inst = tuple(instantiate) if isinstance(instantiate, list) else instantiate
  return _batch_jaxpr(closed_jaxpr, axis_size, tuple(in_batched), inst,
                      axis_name, spmd_axis_name, main_type)
