def _scan_impl_unrolled(*args, reverse, length, num_consts, num_carry, linear,
                        f_impl, x_avals, y_avals):
  consts, init, xs = split_list(args, [num_consts, num_carry])

  carry = init
  ys = []

  for i in range(length):
    i_ = length - i - 1 if reverse else i
    x = _map(partial(_index_array, i_), x_avals, xs)
    out = f_impl(*consts, *carry, *x)
    carry, y = split_list(out, [num_carry])
    ys.append(y)

  ys = list(reversed(ys)) if reverse else ys
  ys = list(zip(*ys))
  ys = _map(_stack, y_avals, ys)
  return (*carry, *ys)
