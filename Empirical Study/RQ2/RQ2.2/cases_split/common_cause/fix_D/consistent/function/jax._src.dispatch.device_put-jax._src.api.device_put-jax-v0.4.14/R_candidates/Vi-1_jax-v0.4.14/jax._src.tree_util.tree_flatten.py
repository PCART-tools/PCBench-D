def tree_flatten(tree: Any,
                 is_leaf: Callable[[Any], bool] | None = None
                 ) -> tuple[list[Leaf], PyTreeDef]:
  """Flattens a pytree.

  The flattening order (i.e. the order of elements in the output list)
  is deterministic, corresponding to a left-to-right depth-first tree
  traversal.

  Args:
    tree: a pytree to flatten.
    is_leaf: an optionally specified function that will be called at each
      flattening step. It should return a boolean, with true stopping the
      traversal and the whole subtree being treated as a leaf, and false
      indicating the flattening should traverse the current object.

  Returns:
    A pair where the first element is a list of leaf values and the second
    element is a treedef representing the structure of the flattened tree.
  """
  if default_registry:
    return default_registry.flatten(tree, is_leaf)
  else:
    return pytree.flatten(tree, is_leaf)  # type: ignore
