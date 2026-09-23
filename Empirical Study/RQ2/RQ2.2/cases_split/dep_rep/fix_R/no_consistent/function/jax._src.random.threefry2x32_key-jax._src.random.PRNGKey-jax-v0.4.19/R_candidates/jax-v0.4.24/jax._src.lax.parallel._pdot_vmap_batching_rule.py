def _pdot_vmap_batching_rule(vals_in, dims_in, *, axis_name, pos_contract,
                             pos_batch, precision):
  x, y = vals_in
  (pos_contract, pos_batch), result_batch_dim = lax._dot_general_batch_dim_nums(
      (x.ndim, y.ndim), dims_in, [pos_contract, pos_batch])
  out = pdot_p.bind(x, y, axis_name=axis_name, pos_contract=pos_contract,
                    pos_batch=pos_batch, precision=precision)
  return out, result_batch_dim
