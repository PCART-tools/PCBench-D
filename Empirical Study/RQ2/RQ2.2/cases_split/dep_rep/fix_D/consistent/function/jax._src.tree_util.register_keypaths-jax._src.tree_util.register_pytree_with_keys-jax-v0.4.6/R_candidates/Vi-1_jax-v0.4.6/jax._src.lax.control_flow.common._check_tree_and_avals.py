def _check_tree_and_avals(what, tree1, avals1, tree2, avals2):
  """Raises TypeError if (tree1, avals1) does not match (tree2, avals2).

  Corresponding `tree` and `avals` must match in the sense that the number of
  leaves in `tree` must be equal to the length of `avals`. `what` will be
  prepended to details of the mismatch in TypeError.
  """
  if tree1 != tree2:
    raise TypeError(
        f"{what} must have same type structure, got {tree1} and {tree2}.")
  if not all(map(core.typematch, avals1, avals2)):
    diff = tree_map(_show_diff, tree_unflatten(tree1, avals1),
                    tree_unflatten(tree2, avals2))
    raise TypeError(f"{what} must have identical types, got\n{diff}.")
