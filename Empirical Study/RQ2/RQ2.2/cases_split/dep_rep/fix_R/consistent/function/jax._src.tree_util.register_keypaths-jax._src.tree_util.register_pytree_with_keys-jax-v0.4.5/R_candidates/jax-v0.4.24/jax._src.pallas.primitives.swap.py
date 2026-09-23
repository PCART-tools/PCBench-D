def swap(x_ref_or_view, idx, val, *, mask=None, eviction_policy=None,
         _function_name="swap") -> Any:
  x_ref, indexers = sp.get_ref_and_indexers(x_ref_or_view, idx, _function_name)
  args_flat, args_tree = tree_util.tree_flatten((x_ref, indexers, val, mask))
  return swap_p.bind(
      *args_flat, args_tree=args_tree, eviction_policy=eviction_policy
  )
