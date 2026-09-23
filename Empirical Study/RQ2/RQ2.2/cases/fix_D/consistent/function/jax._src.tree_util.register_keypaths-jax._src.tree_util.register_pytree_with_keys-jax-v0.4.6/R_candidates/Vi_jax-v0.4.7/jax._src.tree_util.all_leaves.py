def all_leaves(iterable: Iterable[Any],
               is_leaf: Optional[Callable[[Any], bool]] = None) -> bool:
  """Tests whether all elements in the given iterable are all leaves.

  >>> tree = {"a": [1, 2, 3]}
  >>> assert all_leaves(jax.tree_util.tree_leaves(tree))
  >>> assert not all_leaves([tree])

  This function is useful in advanced cases, for example if a library allows
  arbitrary map operations on a flat iterable of leaves it may want to check
  if the result is still a flat iterable of leaves.

  Args:
    iterable: Iterable of leaves.

  Returns:
    A boolean indicating if all elements in the input are leaves.
  """
  if is_leaf is None:
    return pytree.all_leaves(iterable)
  else:
    lst = list(iterable)
    return lst == tree_leaves(lst, is_leaf)
