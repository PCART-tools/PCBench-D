def broadcast_prefix(prefix_tree: Any, full_tree: Any,
                     is_leaf: Optional[Callable[[Any], bool]] = None
                     ) -> List[Any]:
  # If prefix_tree is not a tree prefix of full_tree, this code can raise a
  # ValueError; use prefix_errors to find disagreements and raise more precise
  # error messages.
  result = []
  num_leaves = lambda t: tree_structure(t).num_leaves
  add_leaves = lambda x, subtree: result.extend([x] * num_leaves(subtree))
  tree_map(add_leaves, prefix_tree, full_tree, is_leaf=is_leaf)
  return result
