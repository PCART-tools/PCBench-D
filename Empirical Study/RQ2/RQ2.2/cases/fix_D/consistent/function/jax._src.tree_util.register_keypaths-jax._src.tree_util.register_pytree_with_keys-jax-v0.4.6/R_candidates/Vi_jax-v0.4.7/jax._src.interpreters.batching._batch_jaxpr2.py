@weakref_lru_cache
def _batch_jaxpr2(closed_jaxpr: core.ClosedJaxpr,
                 axis_size: core.AxisSize,
                 in_axes: Tuple[Union[int, NotMapped], ...],
                 axis_name: AxisName,
                 spmd_axis_name: AxisName,
                 main_type: Type[BatchTrace],
                 ) -> Tuple[core.ClosedJaxpr, Tuple[Union[int, NotMapped], ...]]:
  f = lu.wrap_init(core.jaxpr_as_fun(closed_jaxpr))
  f, out_axes = _batch_jaxpr_inner(f, axis_size)
  f = _batch_jaxpr_outer(f, axis_name, spmd_axis_name, axis_size, in_axes,
                         main_type)
  avals_in = [core.unmapped_aval(axis_size, axis_name, b, aval)
              if b is not not_mapped else aval
              for aval, b in unsafe_zip(closed_jaxpr.in_avals, in_axes)]
  jaxpr_out, _, consts = pe.trace_to_jaxpr_dynamic(f, avals_in)
  return core.ClosedJaxpr(jaxpr_out, consts), out_axes()
