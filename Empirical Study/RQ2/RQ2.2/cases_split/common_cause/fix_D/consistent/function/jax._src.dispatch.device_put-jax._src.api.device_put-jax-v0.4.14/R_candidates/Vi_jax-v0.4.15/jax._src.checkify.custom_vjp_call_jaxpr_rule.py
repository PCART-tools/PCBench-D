def custom_vjp_call_jaxpr_rule(in_err, enabled_errors, *in_vals, fun_jaxpr,
                               fwd_jaxpr_thunk, num_consts, bwd, out_trees,
                               symbolic_zeros):
  err_vals, err_tree = jtu.tree_flatten(in_err)
  num_errs = err_tree.num_leaves
  checkified_fun = lu.wrap_init(
      functools.partial(checkify_jaxpr_flat, fun_jaxpr.jaxpr,
                        fun_jaxpr.consts, enabled_errors, err_tree))
  checkified_fun, fun_metadata = _flatten_and_get_error_metadata_thunk(
      checkified_fun)

  @lu.wrap_init
  def checkified_fwd(*args):
    # TODO(lenamartens, sharadmv): why not checkify here?
    xs, zeros = args[::2], args[1::2]
    xs, zeros = xs[num_errs:], zeros[num_errs:]
    fwd_jaxpr, fwd_consts = fwd_jaxpr_thunk(*zeros)
    xs_without_consts = xs[num_consts:]
    return core.eval_jaxpr(fwd_jaxpr, fwd_consts, *xs_without_consts)

  bwd_ = lambda *args: (*(None,)*num_errs, *bwd(*args))
  checkified_fwd, fwd_out_tree = flatten_fun_output(checkified_fwd)
  all_outs = custom_derivatives.custom_vjp_call_p.bind(
      checkified_fun, checkified_fwd, bwd_, *err_vals, *in_vals, out_trees=out_trees,
      symbolic_zeros=symbolic_zeros)
  fst, out_metadata = lu.merge_linear_aux(fun_metadata, fwd_out_tree)
  if fst:
    err_and_out_tree, _ = out_metadata
    out_err, out_vals = tree_unflatten(err_and_out_tree, all_outs)
  else:
    out_err, out_vals = in_err, all_outs
  return out_err, out_vals
