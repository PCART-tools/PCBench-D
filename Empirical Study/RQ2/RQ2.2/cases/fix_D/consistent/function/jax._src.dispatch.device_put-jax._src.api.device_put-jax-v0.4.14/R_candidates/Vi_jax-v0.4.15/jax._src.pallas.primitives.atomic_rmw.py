def atomic_rmw(x_ref, idx, val, *, mask: Any | None = None,
               atomic_type: AtomicOpType):
  idx = NDIndexer.from_indices_shape(idx, x_ref.shape)
  args = (idx,)
  if mask is not None:
    args = (*args, mask)
  flat_args, args_tree = tree_util.tree_flatten(args)
  return atomic_rmw_p.bind(x_ref, val, *flat_args, args_tree=args_tree,
                           atomic_type=atomic_type, masked=mask is not None)
