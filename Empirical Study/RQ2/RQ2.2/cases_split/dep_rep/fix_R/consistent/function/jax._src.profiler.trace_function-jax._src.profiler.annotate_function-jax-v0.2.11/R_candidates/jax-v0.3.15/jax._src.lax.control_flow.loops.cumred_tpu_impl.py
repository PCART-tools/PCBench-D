def cumred_tpu_impl(window_reduce: Callable, x, *, axis: int, reverse: bool):
  # On TPU, an implementation using reduce_window is handled specially by the
  # compiler and is efficient. On other backends, it is O(n^2).
  n = x.shape[axis]
  if n == 0:
    return x
  padding = [(0, 0)] * x.ndim
  padding[axis] = (0, n - 1) if reverse else (n - 1, 0)
  strides = [1] * x.ndim
  window_dims = [1] * x.ndim
  window_dims[axis] = n
  return window_reduce(x, window_dims, strides, padding)
