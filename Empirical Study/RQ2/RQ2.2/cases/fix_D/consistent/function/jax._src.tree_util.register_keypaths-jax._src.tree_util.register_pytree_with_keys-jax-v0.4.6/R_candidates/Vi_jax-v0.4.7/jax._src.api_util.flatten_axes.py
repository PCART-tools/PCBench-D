def flatten_axes(name, treedef, axis_tree, *, kws=False, tupled_args=False):
  # given an axis spec tree axis_tree (a pytree with integers and Nones at the
  # leaves, i.e. the Nones are to be considered leaves) that is a tree prefix of
  # the given treedef, build a complete axis spec tree with the same structure
  # and return the flattened result
  # TODO(mattjj,phawkins): improve this implementation

  proxy = object()
  dummy = tree_unflatten(treedef, [object()] * treedef.num_leaves)
  axes = []
  add_leaves = lambda i, x: axes.extend([i] * len(tree_flatten(x)[0]))
  try:
    tree_map(add_leaves, _replace_nones(proxy, axis_tree), dummy)
  except ValueError:
    if kws:
      # if keyword arguments are included in the tree, we make adapt the error
      # message only to be about the positional arguments
      treedef, _ = treedef_children(treedef)
      axis_tree, _ = axis_tree
    hint = ""
    if tupled_args:
      hint += (f" Note that {name} that are non-trivial pytrees should always be "
               f"wrapped in a tuple representing the argument list.")
      if len(treedef.children()) == 1:
        try:
          flatten_axes(name, treedef, (axis_tree,))
        except ValueError:
          pass  # That's not the issue.
        else:
          hint += (f" In particular, you're passing in a single argument which "
                   f"means that {name} might need to be wrapped in "
                   f"a singleton tuple.")
    raise ValueError(f"{name} specification must be a tree prefix of the "
                     f"corresponding value, got specification {axis_tree} "
                     f"for value tree {treedef}.{hint}") from None
  axes = [None if a is proxy else a for a in axes]
  assert len(axes) == treedef.num_leaves
  return axes
