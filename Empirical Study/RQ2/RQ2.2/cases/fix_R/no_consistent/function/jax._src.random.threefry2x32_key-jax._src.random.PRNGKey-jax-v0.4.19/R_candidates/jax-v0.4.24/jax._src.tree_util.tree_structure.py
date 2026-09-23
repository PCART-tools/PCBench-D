def tree_structure(tree: Any,
                   is_leaf: None | (Callable[[Any],
                                              bool]) = None) -> PyTreeDef:
  """Gets the treedef for a pytree."""
  return default_registry.flatten(tree, is_leaf)[1]
