def _transpose_cond_jaxpr(jaxpr, num_res, reduce_axes):
  res_avals, primal_avals = split_list(jaxpr.in_avals, [num_res])
  primal_avals = map(raise_to_shaped, primal_avals)

  @lu.wrap_init
  def transposed(*args):
    res, cts_out = split_list(args, [num_res])
    primals = res + [ad.UndefinedPrimal(aval) for aval in primal_avals]
    cts_in = ad.backward_pass(
        jaxpr.jaxpr, reduce_axes, False, jaxpr.consts, primals, cts_out)
    _, cts_in = split_list(cts_in, [num_res])
    return map(ad.instantiate_zeros_aval, primal_avals, cts_in)

  return _make_closed_jaxpr(transposed, res_avals + jaxpr.out_avals)
