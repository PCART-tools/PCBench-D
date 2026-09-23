def custom_vjp_call_jaxpr_rule(in_err, enabled_errors, *in_vals, fun_jaxpr,
                               fwd_jaxpr_thunk, num_consts, bwd, out_trees):
  err_vals, err_tree = jtu.tree_flatten(in_err)
  fun = lu.wrap_init(
      functools.partial(checkify_jaxpr_flat, fun_jaxpr.jaxpr,
                        fun_jaxpr.consts, enabled_errors, err_tree))
  fun, fun_metadata = _flatten_and_get_error_metadata_thunk(fun)

  @lu.wrap_init
  def fwd(*xs):
    # TODO(lenamartens, sharadmv): why not checkify here?
    fwd_jaxpr, fwd_consts = fwd_jaxpr_thunk()
    xs_without_consts = xs[num_consts:]
    return core.eval_jaxpr(fwd_jaxpr, fwd_consts, *xs_without_consts)

  fwd, fwd_out_tree = flatten_fun_output(fwd)
  all_outs = custom_derivatives.custom_vjp_call_p.bind(
      fun, fwd, bwd, *err_vals, *in_vals, out_trees=out_trees)
  fst, out_metadata = lu.merge_linear_aux(fun_metadata, fwd_out_tree)
  if fst:
    err_and_out_tree, _ = out_metadata
    out_err, out_vals = tree_unflatten(err_and_out_tree, all_outs)
  else:
    err_vals, out_vals = split_list(all_outs, [len(err_vals)])
    # forward input error to output
    out_err = jtu.tree_unflatten(err_tree, err_vals)
  return out_err, out_vals
