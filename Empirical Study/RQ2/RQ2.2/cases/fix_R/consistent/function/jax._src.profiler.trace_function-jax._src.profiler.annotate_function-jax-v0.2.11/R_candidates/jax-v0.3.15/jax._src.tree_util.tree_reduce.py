def tree_reduce(function: Callable[[T, Any], T],
                tree: Any,
                initializer: Any = no_initializer) -> T:
  if initializer is no_initializer:
    return functools.reduce(function, tree_leaves(tree))
  else:
    return functools.reduce(function, tree_leaves(tree), initializer)
