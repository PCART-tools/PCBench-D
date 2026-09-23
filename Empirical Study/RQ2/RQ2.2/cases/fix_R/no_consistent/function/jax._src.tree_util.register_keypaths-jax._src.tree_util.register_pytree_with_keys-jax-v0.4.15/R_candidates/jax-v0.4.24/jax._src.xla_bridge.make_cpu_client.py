def make_cpu_client() -> xla_client.Client:
  if xla_extension_version >= 223:
    collectives: xla_client._xla.CpuCollectives | None = None
    if _CPU_ENABLE_GLOO_COLLECTIVES.value:
      collectives = xla_client._xla.make_gloo_tcp_collectives(  # type: ignore
        distributed_client=distributed.global_state.client,
      )
    return xla_client.make_cpu_client(  # type: ignore
      distributed_client=distributed.global_state.client,
      node_id=distributed.global_state.process_id,
      num_nodes=distributed.global_state.num_processes,
      collectives=collectives,
    )
  elif xla_extension_version >= 216:
    # TODO(phawkins): remove type: ignore after updating jaxlib version used for
    # mypy checks.
    return xla_client.make_cpu_client(  # type: ignore
      distributed_client=distributed.global_state.client,
      node_id=distributed.global_state.process_id,
      num_nodes=distributed.global_state.num_processes,
    )
  else:
    return xla_client.make_cpu_client()
