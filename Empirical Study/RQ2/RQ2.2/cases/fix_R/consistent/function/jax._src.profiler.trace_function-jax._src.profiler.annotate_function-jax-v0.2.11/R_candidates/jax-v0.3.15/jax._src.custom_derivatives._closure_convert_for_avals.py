@cache()
def _closure_convert_for_avals(fun, in_tree, in_avals):
  wrapped_fun, out_tree = flatten_fun_nokwargs(lu.wrap_init(fun), in_tree)
  jaxpr, out_pvals, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, in_avals)
  out_tree = out_tree()

  (closure_consts, hoisted_consts), merge = partition_list(_maybe_perturbed, consts)
  num_consts = len(hoisted_consts)

  def converted_fun(*args_hconsts):
    num_args = len(args_hconsts) - num_consts
    args, hoisted_consts = split_list(args_hconsts, [num_args])
    consts = merge(closure_consts, hoisted_consts)
    all_args, in_tree2 = tree_flatten(tuple(args))
    assert in_tree == in_tree2
    out_flat = core.eval_jaxpr(jaxpr, consts, *all_args)
    return tree_unflatten(out_tree, out_flat)

  return converted_fun, hoisted_consts
