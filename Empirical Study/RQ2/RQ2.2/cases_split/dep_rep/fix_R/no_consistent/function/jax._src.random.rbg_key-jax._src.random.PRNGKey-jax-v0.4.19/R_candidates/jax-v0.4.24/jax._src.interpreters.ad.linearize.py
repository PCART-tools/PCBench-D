def linearize(traceable, *primals, **kwargs):
  has_aux = kwargs.pop('has_aux', False)
  if not has_aux:
    jvpfun = jvp(traceable)
  else:
    jvpfun, aux = jvp(traceable, has_aux=True)

  in_pvals = (tuple(pe.PartialVal.known(p) for p in primals)
              + tuple(pe.PartialVal.unknown(get_aval(p).at_least_vspace())
                      for p in primals))
  _, in_tree = tree_flatten(((primals, primals), {}))
  jvpfun_flat, out_tree = flatten_fun(jvpfun, in_tree)
  jaxpr, out_pvals, consts = pe.trace_to_jaxpr_nounits(jvpfun_flat, in_pvals)
  out_primals_pvals, out_tangents_pvals = tree_unflatten(out_tree(), out_pvals)
  assert all(out_primal_pval.is_known() for out_primal_pval in out_primals_pvals)
  out_primals_consts = [pval.get_known() for pval in out_primals_pvals]
  if not has_aux:
    return out_primals_consts, out_tangents_pvals, jaxpr, consts
  else:
    return out_primals_consts, out_tangents_pvals, jaxpr, consts, aux()
