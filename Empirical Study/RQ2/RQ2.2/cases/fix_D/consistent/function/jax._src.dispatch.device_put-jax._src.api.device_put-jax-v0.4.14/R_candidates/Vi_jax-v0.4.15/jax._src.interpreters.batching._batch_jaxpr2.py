@weakref_lru_cache
def _batch_jaxpr2(
    closed_jaxpr: core.ClosedJaxpr,
    axis_size: core.AxisSize,
    in_axes: tuple[int | NotMapped | RaggedAxis, ...],
    axis_name: AxisName,
    spmd_axis_name: AxisName,
    main_type: type[BatchTrace],
  ) -> tuple[core.ClosedJaxpr, tuple[int | NotMapped, ...]]:
  f = lu.wrap_init(core.jaxpr_as_fun(closed_jaxpr))
  f, out_axes = _batch_jaxpr_inner(f, axis_size)
  f = _batch_jaxpr_outer(f, axis_name, spmd_axis_name, axis_size, in_axes,
                         main_type)
  in_axes2, avals_in = unzip2([
      handle_ragged(closed_jaxpr.in_avals, dim, aval)
      if isinstance(dim, RaggedAxis) else (dim, aval)
      for dim, aval in zip(in_axes, closed_jaxpr.in_avals)])
  avals_in2 = [core.unmapped_aval(axis_size, axis_name, b, aval)
               if b is not not_mapped else aval
               for aval, b in unsafe_zip(avals_in, in_axes2)]
  jaxpr_out, _, consts = pe.trace_to_jaxpr_dynamic(f, avals_in2)
  return core.ClosedJaxpr(jaxpr_out, consts), out_axes()
