def cumred_gpu_impl(window_reduce: Callable, reduce_fn: Callable, x, *,
                    axis: int, reverse: bool):
  # On GPU, reduce_window is executed in a single fusion and associative_scan
  # is split into multiple to materialize intermediate calculations.
  # On small inputs reduce_window is faster being a single fusion,
  # but on larger ones is slower because of O(n^2) complexity.
  # This conservative value of the threshold was obtained via benchmarking.
  if x.shape[axis] > 32:
    return associative_scan(reduce_fn, x, reverse=reverse, axis=axis)
  return cumred_reduce_window_impl(window_reduce, x, axis=axis, reverse=reverse)
