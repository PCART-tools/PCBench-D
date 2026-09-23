def _sharding_constraint_impl(x, sharding, resource_env, unconstrained_dims):
  if hasattr(x, 'sharding') and x.sharding.is_equivalent_to(sharding, x.ndim):
    return x
  # Run a jit here to raise good errors when device assignment don't match.
  return api.jit(_identity_fn, out_shardings=sharding)(x)
