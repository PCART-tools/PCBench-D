def _scan_transpose(reduce_axes, cts, *args, reverse, length, num_consts,
                    num_carry, jaxpr, linear, unroll):
  # we've only implemented transposing scans with specific lin/nonlin patterns
  consts_lin, init_lin, xs_lin = split_list(linear, [num_consts, num_carry])
  num_ires = len(consts_lin) - sum(consts_lin)
  num_eres = len(xs_lin) - sum(xs_lin)
  if consts_lin != [False] * num_ires + [True] * (len(consts_lin) - num_ires):
    raise NotImplementedError
  if xs_lin != [True] * (len(xs_lin) - num_eres) + [False] * num_eres:
    raise NotImplementedError
  if not all(init_lin):
    pass  # TODO(mattjj): error check https://github.com/google/jax/issues/1963

  consts, _, xs = split_list(args, [num_consts, num_carry])
  ires, _ = split_list(consts, [num_ires])
  _, eres = split_list(xs, [sum(xs_lin)])
  assert not any(ad.is_undefined_primal(r) for r in ires)
  assert not any(ad.is_undefined_primal(r) for r in eres)

  carry_avals, y_avals = split_list(jaxpr.out_avals, [num_carry])
  ct_carry, ct_ys = split_list(cts, [num_carry])
  ct_carry = _map(ad.instantiate_zeros, ct_carry)
  ct_ys_is_zeros = tuple(type(ct_y) is ad.Zero for ct_y in ct_ys)
  ct_ys = [x for x in ct_ys if type(x) is not ad.Zero]

  ct_consts = _map(ad_util.zeros_like_aval, jaxpr.in_avals[num_ires:num_consts])

  #       jaxpr :: [ires, T d] -> [T c] -> [T a, eres] -> ([T c], [T b])
  # jaxpr_trans :: [ires] -> [CT d, CT c] -> [CT b, eres] -> ([CT d, CT c], [CT a])
  jaxpr_trans, attrs_tracked = _transpose_scan_jaxpr(
      jaxpr, num_ires, num_consts - num_ires, num_eres, reduce_axes,
      ct_ys_is_zeros)
  linear_trans = ([False] * num_ires + [False] * len(attrs_tracked) +
                  [True] * (len(ct_consts) + len(ct_carry) + len(ct_ys)) +
                  [False] * num_eres)
  in_state = _get_states(attrs_tracked)
  outs = scan_p.bind(
      *ires, *in_state, *ct_consts, *ct_carry, *ct_ys, *eres,
      reverse=not reverse, length=length, jaxpr=jaxpr_trans,
      num_consts=num_ires,
      num_carry=num_consts-num_ires+num_carry+len(attrs_tracked),
      linear=tuple(linear_trans), unroll=unroll)
  out_state, outs = split_list(outs, [len(attrs_tracked)])
  _set_states(attrs_tracked, out_state)
  ct_consts, ct_init, ct_xs = split_list(outs, [num_consts - num_ires, num_carry])
  return [None] * num_ires + ct_consts + ct_init + ct_xs + [None] * num_eres
