def equality_errors(
    tree1: Any, tree2: Any, is_leaf: Optional[Callable[[Any], bool]] = None,
) -> Iterable[Tuple[KeyPath, str, str, str]]:
  yield from _equality_errors((), tree1, tree2, is_leaf)
