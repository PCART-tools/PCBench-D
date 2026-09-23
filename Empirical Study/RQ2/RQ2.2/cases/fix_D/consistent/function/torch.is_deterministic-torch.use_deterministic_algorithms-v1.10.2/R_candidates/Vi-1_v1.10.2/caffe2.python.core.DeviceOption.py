def DeviceOption(
    device_type,
    device_id=0,
    random_seed=None,
    node_name=None,
    numa_node_id=None,
    extra_info=None,
):
    option = caffe2_pb2.DeviceOption()
    option.device_type = device_type
    option.device_id = device_id
    if node_name is not None:
        option.node_name = node_name
    if random_seed is not None:
        option.random_seed = random_seed
    if numa_node_id is not None:
        assert device_type == caffe2_pb2.CPU
        option.numa_node_id = numa_node_id
    if extra_info is not None:
        option.extra_info.extend(extra_info)
    return option
