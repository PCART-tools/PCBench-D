def tree_map(f: Callable[..., Any],
             tree: Any,
             *rest: Any,
             is_leaf: Callable[[Any], bool] | None = None) -> Any:
  """Maps a multi-input function over pytree args to produce a new pytree.

  Args:
    f: function that takes ``1 + len(rest)`` arguments, to be applied at the
      corresponding leaves of the pytrees.
    tree: a pytree to be mapped over, with each leaf providing the first
      positional argument to ``f``.
    rest: a tuple of pytrees, each of which has the same structure as ``tree``
      or has ``tree`` as a prefix.
    is_leaf: an optionally specified function that will be called at each
      flattening step. It should return a boolean, which indicates whether the
      flattening should traverse the current object, or if it should be stopped
      immediately, with the whole subtree being treated as a leaf.

  Returns:
    A new pytree with the same structure as ``tree`` but with the value at each
    leaf given by ``f(x, *xs)`` where ``x`` is the value at the corresponding
    leaf in ``tree`` and ``xs`` is the tuple of values at corresponding nodes in
    ``rest``.

  Examples:

    >>> import jax.tree_util
    >>> jax.tree_util.tree_map(lambda x: x + 1, {"x": 7, "y": 42})
    {'x': 8, 'y': 43}

    If multiple inputs are passed, the structure of the tree is taken from the
    first input; subsequent inputs need only have ``tree`` as a prefix:

    >>> jax.tree_util.tree_map(lambda x, y: [x] + y, [5, 6], [[7, 9], [1, 2]])
    [[5, 7, 9], [6, 1, 2]]
  """
  leaves, treedef = tree_flatten(tree, is_leaf)
  all_leaves = [leaves] + [treedef.flatten_up_to(r) for r in rest]
  return treedef.unflatten(f(*xs) for xs in zip(*all_leaves))
