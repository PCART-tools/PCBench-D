@weakref_lru_cache
def _transpose_scan_jaxpr(jaxpr, num_res1, num_c, num_res2, reduce_axes,
                          ct_ys_is_zeros):
  num_a = len(jaxpr.in_avals) - num_res1 - num_c - num_res2
  # TODO: allow input cotangent avals to be batched relative to jaxpr.in_avals
  # if an axis isn't reduced
  res1_avals, c_avals, a_avals, res2_avals = split_list(
      jaxpr.in_avals, [num_res1, num_c, num_a])

  num_ys = len(ct_ys_is_zeros)
  num_b = len(jaxpr.out_avals) - num_ys
  # TODO: Also propagate ad.Zero through b_carry_avals until fixed point.
  b_carry_avals, b_ys_avals = split_list(list(jaxpr.out_avals), [num_b])
  b_ys_avals_stripped = [
      aval for aval, is_zero in zip(b_ys_avals, ct_ys_is_zeros) if not is_zero
  ]

  @lu.wrap_init
  def transposed(*res1_cbar_bbar_res2):
    res1, c_bar, b_bar, ys_bar_stripped, res2 = split_list(
        res1_cbar_bbar_res2,
        [num_res1, num_c, num_b, len(b_ys_avals_stripped)])
    ys_bar_stripped_iter = iter(ys_bar_stripped)
    ys_bar = [
        ad.Zero(aval) if is_zero else next(ys_bar_stripped_iter)
        for aval, is_zero in zip(b_ys_avals, ct_ys_is_zeros)
    ]
    # TODO(mattjj): c_avals should be _tangent_ types here...
    primals = (res1 + [ad.UndefinedPrimal(aval) for aval in c_avals] +
               [ad.UndefinedPrimal(aval) for aval in a_avals] + res2)
    cbar_abar = ad.backward_pass(
        jaxpr.jaxpr, reduce_axes, False, jaxpr.consts, primals, b_bar + ys_bar)
    _, new_c_bar, a_bar, _ = split_list(cbar_abar, [num_res1, num_c, num_a])
    a_bar = _map(ad.instantiate_zeros, a_bar)
    c_bar = _map(ad.instantiate_zeros, _map(ad.add_tangents, c_bar, new_c_bar))
    return c_bar + a_bar
  return _make_closed_jaxpr_attrs(
      transposed, tuple(res1_avals + c_avals + b_carry_avals +
                        b_ys_avals_stripped + res2_avals))
