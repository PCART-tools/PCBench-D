def stage_parallel_callable(
    pci: ParallelCallableInfo,
    fun: lu.WrappedFun,
    global_arg_shapes: Sequence[Optional[Tuple[int, ...]]]):
  sharded_avals = tuple(
      shard_aval(pci.axis_size, axis, aval) if axis is not None else aval
      for axis, aval in safe_zip(pci.in_axes, pci.avals))
  if any(s is not None for s in global_arg_shapes):
    # TODO(skye): we could take this branch unconditionally if we handled
    # grad of global_arg_shapes correctly.
    global_sharded_avals = [
        aval.update(shape=shape) if shape is not None else aval
        for shape, aval in safe_zip(global_arg_shapes, sharded_avals)]
  else:
    global_sharded_avals = sharded_avals  # type: ignore

  with core.extend_axis_env(pci.axis_name, pci.global_axis_size, None):  # type: ignore
    with dispatch.log_elapsed_time(f"Finished tracing + transforming {fun.__name__} "
                                   "for pmap in {elapsed_time} sec",
                                   event=dispatch.JAXPR_TRACE_EVENT):
      jaxpr, out_sharded_avals, consts = pe.trace_to_jaxpr_final(
          fun, global_sharded_avals, pe.debug_info_final(fun, "pmap"))
  jaxpr = dispatch.apply_outfeed_rewriter(jaxpr)

  assert len(out_sharded_avals) == len(pci.out_axes), (
      len(out_sharded_avals), len(pci.out_axes))

  # TODO(skye,mattjj): allow more collectives on multi-host as we test them, but
  # for now raise an error
  if pci.devices is not None:
    is_multi_host_pmap = len(pci.local_devices) != len(pci.devices)
  else:
    is_multi_host_pmap = xb.process_count(pci.backend) > 1
  if is_multi_host_pmap:
    check_multihost_collective_allowlist(jaxpr)

  replicas = find_replicas(jaxpr, pci.axis_size, pci.global_axis_size)
  parts = find_partitions(jaxpr)

  num_local_shards = replicas.num_local_replicas * parts.local_num_partitions
  num_global_shards = replicas.num_global_replicas * parts.num_partitions

  shards = ShardInfo(
      sharded_avals, out_sharded_avals, global_sharded_avals,
      num_local_shards, num_global_shards)

  return jaxpr, consts, replicas, parts, shards
