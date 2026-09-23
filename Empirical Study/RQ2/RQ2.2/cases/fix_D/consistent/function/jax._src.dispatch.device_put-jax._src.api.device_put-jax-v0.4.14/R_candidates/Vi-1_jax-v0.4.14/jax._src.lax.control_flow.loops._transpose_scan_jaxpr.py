def _transpose_scan_jaxpr(num_res1, num_c, num_res2, jaxpr, reduce_axes):
  num_a = len(jaxpr.in_avals) - num_res1 - num_c - num_res2
  # TODO: allow input cotangent avals to be batched relative to jaxpr.in_avals
  # if an axis isn't reduced
  res1_avals, c_avals, a_avals, res2_avals = split_list(
      jaxpr.in_avals, [num_res1, num_c, num_a])
  num_b = len(jaxpr.out_avals)
  b_avals = list(jaxpr.out_avals)

  @lu.wrap_init
  def transposed(*res1_cbar_bbar_res2):
    res1, c_bar, b_bar, res2 = split_list(
        res1_cbar_bbar_res2, [num_res1, num_c, num_b])
    primals = (res1 + [ad.UndefinedPrimal(aval) for aval in c_avals] +
               [ad.UndefinedPrimal(aval) for aval in a_avals] + res2)
    cbar_abar = ad.backward_pass(jaxpr.jaxpr, reduce_axes, False, jaxpr.consts,
                                 primals, b_bar)
    _, new_c_bar, a_bar, _ = split_list(cbar_abar, [num_res1, num_c, num_a])
    a_bar = _map(ad.instantiate_zeros_aval, a_avals, a_bar)
    c_bar = _map(ad.instantiate_zeros_aval, c_avals,
                _map(ad.add_tangents, c_bar, new_c_bar))
    return c_bar + a_bar
  return _make_closed_jaxpr(transposed, res1_avals + c_avals + b_avals + res2_avals)
