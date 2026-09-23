def generate_key_paths(
    tree: Any, is_leaf: Callable[[Any], bool] | None = None
) -> list[tuple[KeyPath, Any]]:
  return list(_generate_key_paths_((), tree, is_leaf))
