def tree_transpose(outer_treedef: PyTreeDef,
                   inner_treedef: PyTreeDef,
                   pytree_to_transpose: Any) -> Any:
  """Transform a tree having tree structure (outer, inner) into one having structure
  (inner, outer).
  """
  flat, treedef = tree_flatten(pytree_to_transpose)
  inner_size = inner_treedef.num_leaves
  outer_size = outer_treedef.num_leaves
  if treedef.num_leaves != (inner_size * outer_size):
    expected_treedef = outer_treedef.compose(inner_treedef)
    raise TypeError(f"Mismatch\n{treedef}\n != \n{expected_treedef}")
  iter_flat = iter(flat)
  lol = [[next(iter_flat) for _ in range(inner_size)] for __ in range(outer_size)]
  transposed_lol = zip(*lol)
  subtrees = map(partial(tree_unflatten, outer_treedef), transposed_lol)
  return tree_unflatten(inner_treedef, subtrees)
