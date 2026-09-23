def make_trt_module():
    import tensorrt as trt
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network()

    x = network.add_input("x", shape=(1, 2, 3), dtype=trt.float32)
    layer = network.add_elementwise(x, x, trt.ElementWiseOperation.SUM)
    layer.name = "add"
    output = layer.get_output(0)
    output.name = "output"
    network.mark_output(output)
    output.dtype = trt.float32

    builder.max_batch_size = 1024
    builder_config = builder.create_builder_config()
    builder_config.max_workspace_size = 1 << 25
    # Test engine can be serialized and loaded correctly.
    serialized_engine = pickle.dumps(builder.build_engine(network, builder_config))
    return TestTRTModule(pickle.loads(serialized_engine), ["x"], ["output"])
