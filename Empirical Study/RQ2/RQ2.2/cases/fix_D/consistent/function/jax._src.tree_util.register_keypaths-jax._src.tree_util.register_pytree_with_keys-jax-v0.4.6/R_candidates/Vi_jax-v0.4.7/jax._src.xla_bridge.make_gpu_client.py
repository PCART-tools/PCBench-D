def make_gpu_client(
    *, platform_name: str, visible_devices_flag: str
) -> xla_client.Client:
  visible_devices = getattr(FLAGS, visible_devices_flag, "all")
  allowed_devices = None
  if visible_devices != "all":
    allowed_devices = {int(x) for x in visible_devices.split(",")}
  return xla_client.make_gpu_client(
    distributed_client=distributed.global_state.client,
    node_id=distributed.global_state.process_id,
    platform_name=platform_name,
    allowed_devices=allowed_devices)
