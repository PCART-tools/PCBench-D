def _axis_index_lowering(ctx, *, axis_name):
  return [_build_axis_index_lowering_mhlo(axis_name,
                                          ctx.module_context.axis_env)]
