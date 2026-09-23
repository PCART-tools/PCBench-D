def tree_structure(tree, is_leaf: Optional[Callable[[Any], bool]] = None):
  """Gets the treedef for a pytree."""
  return pytree.flatten(tree, is_leaf)[1]
