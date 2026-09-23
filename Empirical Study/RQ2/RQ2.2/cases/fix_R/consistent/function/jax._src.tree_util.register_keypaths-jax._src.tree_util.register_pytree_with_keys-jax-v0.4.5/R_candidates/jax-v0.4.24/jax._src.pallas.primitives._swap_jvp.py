def _swap_jvp(primals, tangents, *, args_tree, **params):
  ref_primal, indexers, val_primal, mask = args_tree.unflatten(primals)
  ref_tangent, _, val_tangent, _ = args_tree.unflatten(tangents)
  val_tangent = ad_util.instantiate(val_tangent)
  return (
      swap_p.bind(
          *tree_util.flatten(ref_primal, indexers, val_primal, mask),
          args_tree=args_tree,
          **params,
      ),
      swap_p.bind(
          *tree_util.flatten(ref_tangent, indexers, val_tangent, mask),
          args_tree=args_tree,
          **params,
      ),
  )
