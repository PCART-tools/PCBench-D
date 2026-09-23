def _scan_impl(*args, reverse, length, num_consts, num_carry, jaxpr, linear,
               unroll):
  _, _, x_avals = split_list(jaxpr.in_avals, [num_consts, num_carry])
  _, y_avals = split_list(jaxpr.out_avals, [num_carry])
  f_impl = core.jaxpr_as_fun(jaxpr)

  if unroll == 1:
    return _scan_impl_loop(
        *args, reverse=reverse, length=length, num_consts=num_consts,
        num_carry=num_carry, linear=linear, f_impl=f_impl, x_avals=x_avals,
        y_avals=y_avals)

  consts, init, xs = split_list(args, [num_consts, num_carry])
  num_blocks, rem = divmod(length, unroll)
  length_div = num_blocks * unroll

  if rem > 0:
    if reverse:
      split = partial(_split_leading_dim, rem)
      xs_rem, xs = unzip2(_map(split, x_avals, xs))
    else:
      split = partial(_split_leading_dim, length_div)
      xs, xs_rem = unzip2(_map(split, x_avals, xs))

  outs = _scan_impl_block_unrolled(
      *consts, *init, *xs, reverse=reverse, length=length_div,
      num_consts=num_consts, num_carry=num_carry, linear=linear,
      block_length=unroll, f_impl=f_impl, x_avals=x_avals, y_avals=y_avals)

  carry, ys = split_list(outs, [num_carry])

  if rem > 0:
    outs = _scan_impl_unrolled(
        *consts, *carry, *xs_rem, reverse=reverse, length=rem,
        num_consts=num_consts, num_carry=num_carry, linear=linear,
        f_impl=f_impl, x_avals=x_avals, y_avals=y_avals)
    carry, ys_rem = split_list(outs, [num_carry])
    if reverse:
      ys = _map(_concatenate, y_avals, ys_rem, ys)
    else:
      ys = _map(_concatenate, y_avals, ys, ys_rem)

  return (*carry, *ys)
