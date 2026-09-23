@lu.transformation
def _match_axes_and_sum(axis_size, axis_name, out_dims_thunk, out_dim_dests, *in_vals):
  # this is like _match_axes, but we do reduce-sums as needed
  out_vals = yield in_vals, {}
  yield map(partial(_matchaxis_symbolic_zeros, axis_name, axis_size, axis_name,
                    sum_match=True), out_dims_thunk(), out_dim_dests, out_vals)
