def _std_basis(pytree):
  import jax.numpy as jnp
  leaves, _ = tree_flatten(pytree)
  ndim = sum(map(np.size, leaves))
  dtype = dtypes.result_type(*leaves)
  flat_basis = jnp.eye(ndim, dtype=dtype)
  return _unravel_array_into_pytree(pytree, 1, None, flat_basis)
