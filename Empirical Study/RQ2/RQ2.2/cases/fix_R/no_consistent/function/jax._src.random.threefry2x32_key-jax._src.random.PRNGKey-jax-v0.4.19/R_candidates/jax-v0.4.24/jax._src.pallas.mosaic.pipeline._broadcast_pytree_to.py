def _broadcast_pytree_to(name: str, from_pytree: Any, to_pytree: Any) -> Any:
  """Broadcasts a prefix-pytree of to_pytree, to the shape of to_pytree.

  Useful for supporting passing in prefixes of things as arguments, like in
  jax.vmap.

  Args:
    name: Name for error messages.
    from_pytree: Prefix tree.
    to_pytree: Target pytree.

  Returns:
    Broadcasted pytree.
  """
  to_treedef = tree_util.tree_structure(to_pytree)
  return tree_util.tree_unflatten(
      to_treedef, flatten_axes(name, to_treedef, from_pytree)
  )
