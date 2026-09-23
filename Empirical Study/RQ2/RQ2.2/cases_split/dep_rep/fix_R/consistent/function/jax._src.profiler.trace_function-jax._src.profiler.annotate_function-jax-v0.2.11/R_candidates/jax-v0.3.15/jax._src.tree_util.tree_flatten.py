def tree_flatten(tree, is_leaf: Optional[Callable[[Any], bool]] = None):
  """Flattens a pytree.

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
  return pytree.flatten(tree, is_leaf)
