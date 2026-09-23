def make_gpu_client(
    *, platform_name: str, visible_devices_flag: jax_config.FlagHolder[str]
) -> xla_client.Client:
  visible_devices = visible_devices_flag.value
  allowed_devices = None
  if visible_devices != "all":
    allowed_devices = {int(x) for x in visible_devices.split(",")}

  return xla_client.make_gpu_client(
      distributed_client=distributed.global_state.client,
      node_id=distributed.global_state.process_id,
      num_nodes=distributed.global_state.num_processes,
      platform_name=platform_name,
      allowed_devices=allowed_devices,
  )
