def _cumulative_reduction_primitive(name, reduce_fn, reduce_window_fn):
  reducer_p = lax.standard_primitive(
    _cumred_shape_rule, partial(_cumred_dtype_rule, name),
    name)
  batching.primitive_batchers[reducer_p] = partial(_cumred_batch_rule,
                                                   reducer_p)

  def register_lowering(fn, platform=None):
    mlir.register_lowering(
        reducer_p,
        mlir.cache_lowering(mlir.lower_fun(fn, multiple_results=False)),
        platform=platform)

  # Default for platforms not treated specially below.
  register_lowering(partial(associative_scan, reduce_fn))
  # On GPU, we choose between window reduction and associative scan
  # based on the input size.
  for platform in ['cuda', 'rocm']:
    register_lowering(
        partial(cumred_gpu_impl, reduce_window_fn, reduce_fn), platform)
  # On TPU, an implementation using reduce_window is handled specially by the
  # compiler and is efficient. On other backends, it is O(n^2).
  register_lowering(partial(cumred_reduce_window_impl, reduce_window_fn), 'tpu')
  return reducer_p
