def _pdot_vmap_collective_rule(axis_size, frame_name, _, vals_in, dims_in, *, axis_name,
                               pos_contract, pos_batch, precision):
  x, y = vals_in
  x_dim, y_dim = dims_in
  x_pos_contract, y_pos_contract = pos_contract
  x_pos_contract = [x_dim] + [d + (d >= x_dim) for d in x_pos_contract]
  y_pos_contract = [y_dim] + [d + (d >= y_dim) for d in y_pos_contract]
  x_pos_batch, y_pos_batch = pos_batch
  x_pos_batch = [d + (d >= x_dim) for d in x_pos_batch]
  y_pos_batch = [d + (d >= y_dim) for d in y_pos_batch]
  remaining_axis_names = tuple(n for n in axis_name if n != frame_name)
  out = pdot_p.bind(x, y, axis_name=remaining_axis_names,
                    pos_contract=(tuple(x_pos_contract), tuple(y_pos_contract)),
                    pos_batch=(tuple(x_pos_batch), tuple(y_pos_batch)),
                    precision=precision)
  return out, None
