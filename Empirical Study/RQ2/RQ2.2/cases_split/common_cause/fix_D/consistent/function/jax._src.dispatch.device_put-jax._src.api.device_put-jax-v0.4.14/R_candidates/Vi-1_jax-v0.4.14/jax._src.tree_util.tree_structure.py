def tree_structure(tree: Any,
                   is_leaf: None | (Callable[[Any],
                                              bool]) = None) -> PyTreeDef:
  """Gets the treedef for a pytree."""
  if default_registry:
    return default_registry.flatten(tree, is_leaf)[1]
  else:
    return pytree.flatten(tree, is_leaf)[1]  # type: ignore
