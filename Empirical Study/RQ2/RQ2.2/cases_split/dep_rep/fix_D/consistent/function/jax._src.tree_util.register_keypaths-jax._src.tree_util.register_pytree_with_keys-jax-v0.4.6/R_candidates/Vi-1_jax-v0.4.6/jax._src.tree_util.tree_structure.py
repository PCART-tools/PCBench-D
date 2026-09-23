def tree_structure(tree: Any,
                   is_leaf: Optional[Callable[[Any], bool]] = None) -> PyTreeDef:
  """Gets the treedef for a pytree."""
  return pytree.flatten(tree, is_leaf)[1]
