def assert_batching_rule(batched_args, batch_dims, *, msgs):
  size = next(x.shape[dim] for x, dim in zip(batched_args, batch_dims)
              if dim is not batching.not_mapped)
  pred, code, payload = (batching.bdim_at_front(a, d, size)
                         for a, d in zip(batched_args, batch_dims))
  err = Error(jnp.logical_not(pred), code, msgs, payload)
  check_error(err)
  return [], []
