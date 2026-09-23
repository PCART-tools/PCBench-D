def _maybe_broadcast(target_shape, x):
  x_shape = np.shape(x)
  if core.symbolic_equal_shape(x_shape, target_shape):
    return x
  elif not x_shape:
    return broadcast_in_dim(x, target_shape, ())
  else:
    dims = [i for i, (a, b) in enumerate(zip(x_shape, target_shape))
            if core.symbolic_equal_dim(a, b)]
    squeeze_shape = [x_shape[i] for i in dims]
    return broadcast_in_dim(reshape(x, squeeze_shape), target_shape, dims)
