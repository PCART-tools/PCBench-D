def tree_leaves(tree: Any,
                is_leaf: Optional[Callable[[Any], bool]] = None
                ) -> List[Leaf]:
  """Gets the leaves of a pytree."""
  return pytree.flatten(tree, is_leaf)[0]
