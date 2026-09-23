def _broadcast_in_dim_partial_eval(
    trace, operand, *dyn_shape, shape, broadcast_dimensions):
  if not dyn_shape:
    return trace.default_process_primitive(
        broadcast_in_dim_p, (operand, *dyn_shape),
        dict(shape=shape, broadcast_dimensions=broadcast_dimensions))
  assert all(t.pval.is_known() for t in dyn_shape)
  operand_tracer = trace.instantiate_const(operand)
  dyn_shape_tracers = map(trace.instantiate_const, dyn_shape)
  dyn_shape_tracers_ = iter(dyn_shape_tracers)
  shape_ = [next(dyn_shape_tracers_) if d is None else d for d in shape]
  out_aval = core.DShapedArray(tuple(shape_), operand.dtype, operand.weak_type)
  out_tracer = pe.JaxprTracer(trace, pe.PartialVal.unknown(out_aval), None)
  eqn = pe.new_eqn_recipe(
      [operand_tracer, *dyn_shape_tracers], [out_tracer], broadcast_in_dim_p,
      dict(shape=shape, broadcast_dimensions=broadcast_dimensions),
      core.no_effects, source_info_util.current())
  out_tracer.recipe = eqn
  return out_tracer
