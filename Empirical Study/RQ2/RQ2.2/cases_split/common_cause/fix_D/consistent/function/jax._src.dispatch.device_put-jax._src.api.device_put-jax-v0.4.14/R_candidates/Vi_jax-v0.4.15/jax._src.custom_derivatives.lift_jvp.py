def lift_jvp(num_consts: int, jvp_jaxpr_thunk: Callable) -> lu.WrappedFun:
  @lu.wrap_init
  def jvp(*xs):
    n, ragged = divmod(len(xs), 2)
    assert not ragged
    primals, tangents = xs[num_consts:n], xs[n+num_consts:]
    zeros = [type(t) is SymbolicZero for t in tangents]
    jvp_jaxpr, jvp_consts, out_zeros = jvp_jaxpr_thunk(*zeros)
    nonzero_tangents = [t for t in tangents if type(t) is not SymbolicZero]
    out = core.eval_jaxpr(jvp_jaxpr, jvp_consts, *primals, *nonzero_tangents)
    out_primals, nz_out_tangents = split_list(out, [len(out_zeros)])
    nz_out_tangents_ = iter(nz_out_tangents)
    out_tangents = [SymbolicZero(core.get_aval(p).at_least_vspace())
                    if z else next(nz_out_tangents_)
                    for p, z in zip(out_primals, out_zeros)]
    assert next(nz_out_tangents_, None) is None
    return [*out_primals, *out_tangents]
  return jvp
