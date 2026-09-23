def batch_jaxpr2(closed_jaxpr: core.ClosedJaxpr,
                 axis_size: core.AxisSize,
                 in_axes: Tuple[Union[int, NotMapped], ...],
                 axis_name: AxisName,
                 spmd_axis_name: AxisName,
                 main_type: Type[BatchTrace],
                 ) -> Tuple[core.ClosedJaxpr, Tuple[Union[int, NotMapped], ...]]:
  return _batch_jaxpr2(closed_jaxpr, axis_size, tuple(in_axes), axis_name,
                       spmd_axis_name, main_type)
