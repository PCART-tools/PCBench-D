def batch_jaxpr_axes(closed_jaxpr, axis_size, in_axes, out_axes_dest, axis_name,
                     spmd_axis_name, main_type):
  return _batch_jaxpr_axes(closed_jaxpr, axis_size, tuple(in_axes),
                           tuple(out_axes_dest), axis_name, spmd_axis_name,
                           main_type)
