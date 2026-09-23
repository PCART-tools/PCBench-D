def stage_parallel_callable(
    pci: ParallelCallableInfo, fun: lu.WrappedFun
) -> tuple[core.Jaxpr, list[Any], ReplicaInfo, ShardInfo]:
  sharded_avals = tuple(
      _shard_aval(pci.axis_size, axis, aval) if axis is not None else aval
      for axis, aval in safe_zip(pci.in_axes, pci.avals))

  orig_fun = fun
  if config.pmap_no_rank_reduction.value:
    fun = _change_argument_ranks(fun, pci.in_axes, pci.out_axes_thunk)
  else:
    fun = orig_fun
  with core.extend_axis_env(pci.axis_name, pci.global_axis_size, None):  # type: ignore
    with dispatch.log_elapsed_time(
        "Finished tracing + transforming {fun_name} for pmap in {elapsed_time} sec",
        fun_name=fun.__name__, event=dispatch.JAXPR_TRACE_EVENT):
      jaxpr, out_sharded_avals, consts = pe.trace_to_jaxpr_final(
          fun, sharded_avals, pe.debug_info_final(fun, "pmap"))
  jaxpr = api_util.jaxpr_debug_info(jaxpr, orig_fun.debug_info)
  jaxpr = dispatch.apply_outfeed_rewriter(jaxpr)

  assert len(out_sharded_avals) == len(pci.out_axes), (
      len(out_sharded_avals), len(pci.out_axes))

  replicas = find_replicas(jaxpr, pci.axis_size, pci.global_axis_size)
  num_local_shards = replicas.num_local_replicas
  num_global_shards = replicas.num_global_replicas

  shards = ShardInfo(
      sharded_avals, out_sharded_avals, sharded_avals,
      num_local_shards, num_global_shards)

  return jaxpr, consts, replicas, shards
