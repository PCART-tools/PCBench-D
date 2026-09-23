def _scan_impl_loop(*args, reverse, length, num_consts, num_carry, linear,
                    f_impl, x_avals, y_avals):
  consts, init, xs = split_list(args, [num_consts, num_carry])

  def cond_fun(vals):
    i, *_ = vals
    return i < length

  def body_fun(vals):
    [i], carry, ys = split_list(vals, [1, num_carry])
    i_ = length - i - 1 if reverse else i
    x = _map(partial(_dynamic_index_array, i_), x_avals, xs)
    out_flat = f_impl(*consts, *carry, *x)
    carry_out, y_updates = split_list(out_flat, [num_carry])
    ys_out = _map(partial(_update_array, i_), y_avals, ys, y_updates)
    return [i + 1] + carry_out + ys_out

  ys_init = _map(partial(_empty_array, length), y_avals)
  if length == 0:
    return init + ys_init
  else:
    init_val = [lax._const(length, 0)] + init + ys_init
    _, *outs = while_loop(cond_fun, body_fun, init_val)
    return outs
