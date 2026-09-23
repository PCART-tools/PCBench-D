def _is_reduced_on_dim(idx):
  # TODO(yashkatariya): This handles very narrow use case where we know XLA will
  # not return an output with uneven sharding. Remove this after we have the
  # ability to catch uneven shardings in lower_sharding_computation and raise
  # a special exception for that which can be caught here to fallback to
  # bouncing via host.
  if not isinstance(idx, tuple):
    idx = (idx,)
  return all(isinstance(i, int) or
             (isinstance(i, slice) and  i == slice(None)) or
             (isinstance(i, (np.ndarray, jax.Array)) and not i.shape and
              np.issubdtype(i.dtype, np.integer))
             for i in idx)
