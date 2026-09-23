def tree_leaves(tree: Any,
                is_leaf: Callable[[Any], bool] | None = None
                ) -> list[Leaf]:
  """Gets the leaves of a pytree."""
  if default_registry:
    return default_registry.flatten(tree, is_leaf)[0]
  else:
    return pytree.flatten(tree, is_leaf)[0]  # type: ignore
