def _cumulative_reduction_primitive(name,
                                    reduce_fn,
                                    tpu_reduce_window_fn):
  reducer_p = lax.standard_primitive(
    _cumred_shape_rule, partial(_cumred_dtype_rule, name),
    name)
  batching.primitive_batchers[reducer_p] = partial(_cumred_batch_rule,
                                                   reducer_p)
  mlir.register_lowering(
      reducer_p,
      mlir.cache_lowering(
          mlir.lower_fun(partial(associative_scan, reduce_fn),
                         multiple_results=False)))
  mlir.register_lowering(
      reducer_p,
      mlir.lower_fun(partial(cumred_tpu_impl, tpu_reduce_window_fn),
                     multiple_results=False),
      platform='tpu')
  return reducer_p
