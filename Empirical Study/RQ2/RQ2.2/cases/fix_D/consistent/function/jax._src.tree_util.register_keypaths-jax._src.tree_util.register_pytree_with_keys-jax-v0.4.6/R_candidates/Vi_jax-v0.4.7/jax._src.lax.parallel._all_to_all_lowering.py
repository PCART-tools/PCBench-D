def _all_to_all_lowering(ctx, x, *,
                         split_axis, concat_axis, axis_name, axis_index_groups):
  # Workaround for AllToAll not being implemented on CPU.
  replica_groups = _replica_groups(ctx.module_context.axis_env, axis_name,
                                   axis_index_groups)
  if len(replica_groups[0]) == 1:
    return [x]
  elif ((ctx.module_context.platform == "tpu") or
        ((ctx.module_context.platform in ("cuda", "rocm"))
         and (split_axis == 0) and (concat_axis == 0))):
    split_count = len(replica_groups[0])
    if not all(split_count == len(g) for g in replica_groups):
      raise ValueError('Replica groups must be equally sized')
    is_spmd = isinstance(ctx.module_context.axis_context,
                         (mlir.SPMDAxisContext, mlir.ShardingContext))
    if is_spmd:
      # We want to emit the all-gather with global device IDs and a unique
      # channel ID, as otherwise it interprets the devices as replicas instead
      # of partitions - and XLA is configured with only a single replica.
      channel = ctx.module_context.new_channel()
      other_args = dict(
          channel_handle=hlo.ChannelHandle.get(channel,
                                               mlir.DEVICE_TO_DEVICE_TYPE))
    else:
      other_args = {}
    return hlo.AllToAllOp(
        x,
        split_dimension=mlir.i64_attr(split_axis),
        concat_dimension=mlir.i64_attr(concat_axis),
        split_count=mlir.i64_attr(split_count),
        replica_groups=_replica_groups_hlo(replica_groups),
        **other_args).results
  else:
    warnings.warn(
        "all_to_all (and pswapaxes) are only implemented properly for TPUs and GPUs (if "
        "split_axis and concat_axis are both 0). All other backends emulate it using a "
        "very slow and memory intensive algorithm, so expect significant slowdowns."
    )
    lowering = mlir.lower_fun(_all_to_all_via_all_gather,
                              multiple_results=False)
    return lowering(ctx, x,
                    axis_name=axis_name,
                    split_axis=split_axis,
                    concat_axis=concat_axis,
                    axis_index_groups=axis_index_groups)
