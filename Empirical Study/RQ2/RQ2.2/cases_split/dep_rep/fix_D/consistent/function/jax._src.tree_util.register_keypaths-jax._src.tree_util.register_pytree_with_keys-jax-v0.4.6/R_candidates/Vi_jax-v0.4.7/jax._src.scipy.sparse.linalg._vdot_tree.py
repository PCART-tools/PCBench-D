def _vdot_tree(x, y):
  return sum(tree_leaves(tree_map(partial(
    jnp.vdot, precision=lax.Precision.HIGHEST), x, y)))
