def swap(x_ref, idx, val, *, mask=None, eviction_policy="") -> Any:
  idx = NDIndexer.from_indices_shape(idx, x_ref.shape)
  args = (idx,)
  if mask is not None:
    args = (*args, mask)
  flat_args, args_tree = tree_util.tree_flatten(args)
  return swap_p.bind(x_ref, val, *flat_args, masked=mask is not None,
                     eviction_policy=eviction_policy, args_tree=args_tree)
