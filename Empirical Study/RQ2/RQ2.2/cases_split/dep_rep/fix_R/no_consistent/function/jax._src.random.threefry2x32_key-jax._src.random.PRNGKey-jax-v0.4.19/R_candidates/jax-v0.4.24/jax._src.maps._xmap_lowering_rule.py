def _xmap_lowering_rule(ctx, *args, **kwargs):
  if isinstance(ctx.module_context.axis_context, sharding_impls.SPMDAxisContext):
    if SPMD_LOWERING_MANUAL.value:
      return _xmap_lowering_rule_spmd_manual(ctx, *args, **kwargs)
    else:
      return _xmap_lowering_rule_spmd(ctx, *args, **kwargs)
  # Here ShardingContext is used in place of ReplicaAxisContext because when
  # axis_resources and mesh is not used with xmap, `make_xmap_callable` will
  # go via `dispatch.sharded_lowering` path which sets the context to
  # ShardingContext. sharding_impls.ShardingContext is not used for SPMD.
  elif isinstance(ctx.module_context.axis_context,
                  (sharding_impls.ReplicaAxisContext, sharding_impls.ShardingContext)):
    return _xmap_lowering_rule_replica(ctx, *args, **kwargs)
  else:
    raise AssertionError("Unrecognized axis context type!")
