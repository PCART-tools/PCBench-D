def vjp(traceable, primals, has_aux=False, reduce_axes=()):
  if not has_aux:
    out_primals, pvals, jaxpr, consts = linearize(traceable, *primals)
  else:
    out_primals, pvals, jaxpr, consts, aux = linearize(traceable, *primals, has_aux=True)

  def unbound_vjp(pvals, jaxpr, consts, *cts):
    cts = tuple(ct for ct, pval in zip(cts, pvals) if not pval.is_known())
    dummy_args = [UndefinedPrimal(v.aval) for v in jaxpr.invars]
    arg_cts = backward_pass(jaxpr, reduce_axes, True, consts, dummy_args, cts)
    return map(instantiate_zeros, arg_cts)

  # Ensure that vjp_ is a PyTree so that we can pass it from the forward to the backward
  # pass in a custom VJP.
  vjp_ =  Partial(partial(unbound_vjp, pvals, jaxpr), consts)
  if not has_aux:
    return out_primals, vjp_
  else:
    return out_primals, vjp_, aux
