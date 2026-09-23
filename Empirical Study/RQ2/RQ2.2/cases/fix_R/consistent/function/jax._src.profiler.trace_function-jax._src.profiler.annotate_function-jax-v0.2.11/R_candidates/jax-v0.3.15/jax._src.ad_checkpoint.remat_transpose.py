def remat_transpose(reduce_axes, out_cts, *in_primals, jaxpr, **params):
  assert not jaxpr.constvars
  cell = lambda: None

  @lu.wrap_init
  def transposed(*args):
    in_primals, out_cts = tree_unflatten(treedef, args)
    in_pvals = [pe.PartialVal.unknown(x.aval) if ad.is_undefined_primal(x) else
                pe.PartialVal.known(x) for x in in_primals]
    primal_fun = lu.wrap_init(partial(core.eval_jaxpr, jaxpr, ()))
    t_jaxpr, _, consts = pe.trace_to_jaxpr_nounits(primal_fun, in_pvals, False)
    dummy_args = [ad.UndefinedPrimal(v.aval) for v in t_jaxpr.invars]
    in_cts = ad.backward_pass(t_jaxpr, reduce_axes, False, consts, dummy_args,
                              out_cts)
    in_cts_ = iter(in_cts)
    in_cts = [next(in_cts_) if ad.is_undefined_primal(x)
              else ad_util.Zero(x.aval) for x in in_primals]
    assert next(in_cts_, None) is None
    in_cts, cell.treedef = tree_flatten(in_cts)
    return in_cts

  args, treedef = tree_flatten((in_primals, out_cts))
  in_avals = [core.raise_to_shaped(core.get_aval(x)) for x in args]
  transposed_jaxpr_, _, consts = pe.trace_to_jaxpr_dynamic(transposed, in_avals)
  transposed_jaxpr = pe.convert_constvars_jaxpr(transposed_jaxpr_)
  in_cts = remat_p.bind(*consts, *args, jaxpr=transposed_jaxpr, **params)
  return tree_unflatten(cell.treedef, in_cts)  # type: ignore
