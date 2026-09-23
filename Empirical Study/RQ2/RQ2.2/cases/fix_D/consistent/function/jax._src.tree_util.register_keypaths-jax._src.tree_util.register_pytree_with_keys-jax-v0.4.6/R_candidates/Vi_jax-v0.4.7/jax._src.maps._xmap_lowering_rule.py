def _xmap_lowering_rule(ctx, *args, **kwargs):
  if isinstance(ctx.module_context.axis_context, mlir.SPMDAxisContext):
    if config.experimental_xmap_spmd_lowering_manual:
      return _xmap_lowering_rule_spmd_manual(ctx, *args, **kwargs)
    else:
      return _xmap_lowering_rule_spmd(ctx, *args, **kwargs)
  # Here ShardingContext is used in place of ReplicaAxisContext because when
  # axis_resources and mesh is not used with xmap, `make_xmap_callable` will
  # go via `dispatch.sharded_lowering` path which sets the context to
  # ShardingContext. mlir.ShardingContext is not used for SPMD.
  elif isinstance(ctx.module_context.axis_context,
                  (mlir.ReplicaAxisContext, mlir.ShardingContext)):
    return _xmap_lowering_rule_replica(ctx, *args, **kwargs)
  else:
    raise AssertionError("Unrecognized axis context type!")
