def _shapes(pytree):
  return map(jnp.shape, tree_leaves(pytree))
