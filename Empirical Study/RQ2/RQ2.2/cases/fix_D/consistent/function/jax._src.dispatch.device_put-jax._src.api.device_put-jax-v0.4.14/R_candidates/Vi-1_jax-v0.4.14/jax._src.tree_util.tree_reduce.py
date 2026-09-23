def tree_reduce(function: Callable[[T, Any], T],
                tree: Any,
                initializer: Any = no_initializer,
                is_leaf: Callable[[Any], bool] | None = None) -> T:
  if initializer is no_initializer:
    return functools.reduce(function, tree_leaves(tree, is_leaf=is_leaf))
  else:
    return functools.reduce(function, tree_leaves(tree, is_leaf=is_leaf), initializer)
