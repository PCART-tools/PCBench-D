def inspect_sharding_partition(shapes, arg_shardings, result_shape,
                               result_sharding, backend_string):
  del result_shape, result_sharding
  sharding_callback_info = sharding_callbacks[backend_string]
  sharding_callback = sharding_callback_info.callback
  module_context = sharding_callback_info.module_context

  # Execute callback
  hlo_sharding, = arg_shardings
  sharding_callback(hlo_sharding)

  tiled_args = [p.tile(s) for s, p in zip(shapes, arg_shardings)]
  in_avals = [core.ShapedArray(arg.dimensions(), arg.numpy_dtype())
              for arg in tiled_args]
  fun = lu.wrap_init(lambda *args: [])
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(fun, in_avals)
  closed_jaxpr = core.ClosedJaxpr(jaxpr, consts)
  trivial_comp = mlir.build_xla_computation_helper(closed_jaxpr,
      name="tmp_xla_computation", platform=module_context.platform,
      backend_or_name=module_context.backend_or_name,
      axis_context=module_context.axis_context)
  # The trivial computation built here has a dummy tuple as the result,
  # so use sharding compatible with it for the result sharding.
  empty_tuple_sharding = xc.OpSharding()
  empty_tuple_sharding.type = xc.OpSharding.Type.TUPLE
  result_sharding = xc.HloSharding.from_proto(empty_tuple_sharding)
  return trivial_comp, arg_shardings, result_sharding
