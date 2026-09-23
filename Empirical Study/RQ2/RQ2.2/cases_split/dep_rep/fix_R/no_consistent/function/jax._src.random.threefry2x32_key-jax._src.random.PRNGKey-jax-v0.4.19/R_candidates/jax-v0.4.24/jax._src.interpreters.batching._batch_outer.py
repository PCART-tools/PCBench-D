@lu.transformation
def _batch_outer(axis_name, axis_size, in_dims, main_type, spmd_axis_name,
                 *in_vals):
  with core.new_main(
      main_type, axis_name=axis_name, spmd_axis_name=spmd_axis_name) as main:
    with core.extend_axis_env(axis_name, axis_size, main):
      with source_info_util.transform_name_stack('vmap'):
        outs = yield (main, in_dims, *in_vals), {}
      del main
  yield outs
