def tree_leaves_with_path(
    tree: Any, is_leaf: Callable[[Any], bool] | None = None
) -> list[tuple[KeyPath, Any]]:
  """Gets the leaves of a pytree like ``tree_leaves`` and returns each leaf's key path.

  Args:
    tree: a pytree. If it contains a custom type, it must be registered with
      ``register_pytree_with_keys``.
  Returns:
    A list of key-leaf pairs, each of which contains a leaf and its key path.
  """
  return _generate_key_paths(tree, is_leaf)
