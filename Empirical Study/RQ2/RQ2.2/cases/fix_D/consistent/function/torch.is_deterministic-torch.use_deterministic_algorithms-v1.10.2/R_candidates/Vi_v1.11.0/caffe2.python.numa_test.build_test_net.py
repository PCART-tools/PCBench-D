def build_test_net(net_name):
    net = core.Net(net_name)
    net.Proto().type = "async_scheduling"

    numa_device_option = caffe2_pb2.DeviceOption()
    numa_device_option.device_type = caffe2_pb2.CPU
    numa_device_option.numa_node_id = 0

    net.ConstantFill([], "output_blob_0", shape=[1], value=3.14,
                         device_option=numa_device_option)

    numa_device_option.numa_node_id = 1
    net.ConstantFill([], "output_blob_1", shape=[1], value=3.14,
                         device_option=numa_device_option)

    gpu_device_option = caffe2_pb2.DeviceOption()
    gpu_device_option.device_type = caffe2_pb2.CUDA
    gpu_device_option.device_id = 0

    net.CopyCPUToGPU("output_blob_0", "output_blob_0_gpu",
                        device_option=gpu_device_option)
    net.CopyCPUToGPU("output_blob_1", "output_blob_1_gpu",
                        device_option=gpu_device_option)

    return net
