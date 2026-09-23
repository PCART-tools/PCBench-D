def atomic_rmw(x_ref_or_view, idx, val, *, mask: Any | None = None,
               atomic_type: AtomicOpType):
  x_ref, indexers = sp.get_ref_and_indexers(x_ref_or_view, idx, "atomic_rmw")
  args_flat, args_tree = tree_util.tree_flatten((x_ref, indexers, val, mask))
  return atomic_rmw_p.bind(
      *args_flat, args_tree=args_tree, atomic_type=atomic_type
  )
