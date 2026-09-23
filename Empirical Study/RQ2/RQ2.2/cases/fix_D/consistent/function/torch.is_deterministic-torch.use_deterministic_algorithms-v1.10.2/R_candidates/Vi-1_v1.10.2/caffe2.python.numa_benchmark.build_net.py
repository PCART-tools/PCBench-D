def build_net(net_name, cross_socket):
    init_net = core.Net(net_name + "_init")
    init_net.Proto().type = "async_scheduling"
    numa_device_option = caffe2_pb2.DeviceOption()
    numa_device_option.device_type = caffe2_pb2.CPU
    numa_device_option.numa_node_id = 0
    for replica_id in range(NUM_REPLICAS):
        init_net.XavierFill([], net_name + "/input_blob_" + str(replica_id),
            shape=[SHAPE_LEN, SHAPE_LEN], device_option=numa_device_option)

    net = core.Net(net_name)
    net.Proto().type = "async_scheduling"
    if cross_socket:
        numa_device_option.numa_node_id = 1
    for replica_id in range(NUM_REPLICAS):
        net.Copy(net_name + "/input_blob_" + str(replica_id),
                net_name + "/output_blob_" + str(replica_id),
                device_option=numa_device_option)
    return init_net, net
