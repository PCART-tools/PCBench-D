def make_gpu_client(
    *, platform_name: str, visible_devices_flag: config.FlagHolder[str]
) -> xla_client.Client:
  visible_devices = visible_devices_flag.value
  allowed_devices = None
  if visible_devices != "all":
    allowed_devices = {int(x) for x in visible_devices.split(",")}

  if platform_name == "cuda":
    _check_cuda_versions()

  use_mock_gpu_client = _USE_MOCK_GPU_CLIENT.value
  num_nodes = (
      _MOCK_NUM_GPUS.value
      if use_mock_gpu_client
      else distributed.global_state.num_processes
  )

  return xla_client.make_gpu_client(
      distributed_client=distributed.global_state.client,
      node_id=distributed.global_state.process_id,
      num_nodes=num_nodes,
      platform_name=platform_name,
      allowed_devices=allowed_devices,
      mock=use_mock_gpu_client,  # type: ignore[call-arg]
  )
