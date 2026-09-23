def make_gpu_client(platform_name=None):
  return xla_client.make_gpu_client(
    distributed_client=distributed.global_state.client,
    node_id=distributed.global_state.process_id,
    platform_name=platform_name)
