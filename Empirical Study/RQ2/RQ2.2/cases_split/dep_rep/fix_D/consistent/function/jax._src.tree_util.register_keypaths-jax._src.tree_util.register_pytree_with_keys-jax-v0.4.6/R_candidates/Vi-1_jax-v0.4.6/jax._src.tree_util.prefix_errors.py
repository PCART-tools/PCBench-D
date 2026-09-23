def prefix_errors(prefix_tree: Any, full_tree: Any,
                  is_leaf: Optional[Callable[[Any], bool]] = None,
                  ) -> List[Callable[[str], ValueError]]:
  return list(_prefix_error((), prefix_tree, full_tree, is_leaf))
