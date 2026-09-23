def _generate_key_paths(
    tree: Any, is_leaf: Optional[Callable[[Any], bool]] = None
) -> List[Tuple[KeyPath, Any]]:
  return list(_generate_key_paths_((), tree, is_leaf))
