def _swap_jvp(primals, tangents, *, args_tree, masked, **params: Any):
  ref_primal, val_primal, *rest_primals = primals
  ref_tangent, val_tangent, *rest_tangents = tangents
  val_tangent = ad_util.instantiate(val_tangent)
  idx_primal, *masked_other_primals = tree_util.tree_unflatten(args_tree, rest_primals)
  flat_idx_primals = tree_util.tree_leaves(idx_primal)
  _, *masked_other_tangents = tree_util.tree_unflatten(args_tree, rest_tangents)
  tangent_args = flat_idx_primals
  if masked:
    tangent_args = [*tangent_args, masked_other_primals[0]]
    if len(masked_other_tangents) == 2:
      _, other_tangent = masked_other_tangents
      other_tangent = ad_util.instantiate(other_tangent)
      tangent_args = [*tangent_args, other_tangent]
  return (
      swap_p.bind(ref_primal, val_primal, *rest_primals, args_tree=args_tree, masked=masked, **params),
      swap_p.bind(ref_tangent, val_tangent, *tangent_args, args_tree=args_tree,
                  masked=masked, **params))
