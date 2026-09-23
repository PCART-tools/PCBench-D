def custom_transpose_transpose_rule(
    cts, *args, out_types, res_tree, lin_tree, out_tree, **params):

  if 'transpose_jaxpr_thunk' in params:
    assert 'call_jaxpr' in params
    transpose = make_transpose_from_thunk(
        params['transpose_jaxpr_thunk'], lin_tree)
  else:
    assert 'call' in params
    transpose = params['transpose']

  call_in_tree = treedef_tuple((res_tree, lin_tree))

  # TODO(frostig,mattjj): `lin_arg` indicates the inputs with respect
  # to which we are transposing (via `ad.is_undefined_primal`).
  # Consider passing this information to the custom transpose rule?

  res_arg, lin_arg = tree_unflatten(call_in_tree, args)
  del lin_arg
  assert all(not ad.is_undefined_primal(x) for x in tree_leaves(res_arg))

  cts = [ad_util.zeros_like_aval(ct.aval) if type(ct) is ad_util.Zero else ct
         for ct in cts]
  ct_out = tree_unflatten(out_tree, cts)
  ct_lin = transpose(res_arg, ct_out)
  check_transpose_rule_trees(transpose, lin_tree, tree_structure(ct_lin))
  ct_lin_flat, _ = tree_flatten(
      tree_broadcast(lin_tree, ct_lin, is_leaf=lambda x: x is None),
      is_leaf=lambda x: x is None)
  return [None] * len(tree_leaves(res_arg)) + ct_lin_flat
