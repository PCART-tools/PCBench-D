@lu.transformation
def _batch_jaxpr_outer(axis_name, spmd_axis_name, axis_size, in_dims, main_type,
                       *in_vals):
  if axis_size is None:
    axis_size, = {x.shape[d] for x, d in zip(in_vals, in_dims) if d is not not_mapped}
  in_dims = in_dims() if callable(in_dims) else in_dims
  in_dims = [canonicalize_axis(ax, np.ndim(x)) if isinstance(ax, int)
             else ax for x, ax in unsafe_zip(in_vals, in_dims)]
  with core.new_main(main_type, axis_name=axis_name,
                     spmd_axis_name=spmd_axis_name) as main:
    with core.extend_axis_env(axis_name, axis_size, main):
      out_vals = yield (main, in_dims, *in_vals), {}
      del main
  yield out_vals
