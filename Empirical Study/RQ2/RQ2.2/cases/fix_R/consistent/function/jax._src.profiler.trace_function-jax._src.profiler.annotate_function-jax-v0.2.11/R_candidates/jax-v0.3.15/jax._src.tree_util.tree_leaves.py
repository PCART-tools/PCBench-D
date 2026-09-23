def tree_leaves(tree, is_leaf: Optional[Callable[[Any], bool]] = None):
  """Gets the leaves of a pytree."""
  return pytree.flatten(tree, is_leaf)[0]
