@weakref_lru_cache
def _batch_jaxpr_axes(closed_jaxpr, axis_size, in_axes, out_axes_dest,
                      axis_name, spmd_axis_name, main_type):
  f = lu.wrap_init(core.jaxpr_as_fun(closed_jaxpr))
  f, out_axes = _batch_jaxpr_inner(f, axis_size)
  f, out_batched = _match_axes_jaxpr(f, axis_size, out_axes_dest, out_axes)
  f = _batch_jaxpr_outer(f, axis_name, spmd_axis_name, axis_size, in_axes,
                         main_type)
  avals_in = [core.unmapped_aval(axis_size, axis_name, b, aval) if b is not not_mapped
              else aval for aval, b in unsafe_zip(closed_jaxpr.in_avals, in_axes)]
  jaxpr_out, _, consts = pe.trace_to_jaxpr_dynamic(f, avals_in)
  return core.ClosedJaxpr(jaxpr_out, consts), out_batched()
