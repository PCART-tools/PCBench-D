def _scan_impl_block_unrolled(*args, reverse, length, num_consts, num_carry,
                              linear, block_length, f_impl, x_avals, y_avals):
  consts, init, xs = split_list(args, [num_consts, num_carry])

  num_blocks, rem = divmod(length, block_length)
  assert rem == 0

  partition = partial(_partition_leading, num_blocks, block_length)
  xs_block = _map(partition, x_avals, xs)

  prepend_aval = partial(_prepend_dim_to_aval, block_length)
  x_block_avals = _map(prepend_aval, x_avals)
  y_block_avals = _map(prepend_aval, y_avals)

  f_impl_block = partial(
      _scan_impl_unrolled, reverse=reverse, length=block_length,
      num_consts=num_consts, num_carry=num_carry, linear=linear,
      f_impl=f_impl, x_avals=x_avals, y_avals=y_avals)

  outs = _scan_impl_loop(
      *consts, *init, *xs_block, reverse=reverse, length=num_blocks,
      num_consts=num_consts, num_carry=num_carry, linear=linear,
      f_impl=f_impl_block, x_avals=x_block_avals, y_avals=y_block_avals)

  carry, ys_blocks = split_list(outs, [num_carry])
  combine = partial(_combine_leading, num_blocks, block_length)
  ys = _map(combine, y_avals, ys_blocks)
  return (*carry, *ys)
