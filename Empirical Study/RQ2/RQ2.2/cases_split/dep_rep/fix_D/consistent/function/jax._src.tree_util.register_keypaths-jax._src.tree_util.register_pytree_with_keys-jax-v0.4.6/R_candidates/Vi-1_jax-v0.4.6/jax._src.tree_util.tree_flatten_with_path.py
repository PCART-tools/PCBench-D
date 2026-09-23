def tree_flatten_with_path(
    tree: Any, is_leaf: Optional[Callable[[Any], bool]] = None
) -> Tuple[List[Tuple[KeyPath, Any]], PyTreeDef]:
  """Flattens a pytree like ``tree_flatten``, but also returns each leaf's key path.

  Args:
    tree: a pytree to flatten. If it contains a custom type, it must be
      registered with ``register_pytree_with_keys``.
  Returns:
    A pair which the first element is a list of key-leaf pairs, each of
    which contains a leaf and its key path. The second element is a treedef
    representing the structure of the flattened tree.
  """
  _, tree_def = tree_flatten(tree, is_leaf)
  return _generate_key_paths(tree, is_leaf), tree_def
