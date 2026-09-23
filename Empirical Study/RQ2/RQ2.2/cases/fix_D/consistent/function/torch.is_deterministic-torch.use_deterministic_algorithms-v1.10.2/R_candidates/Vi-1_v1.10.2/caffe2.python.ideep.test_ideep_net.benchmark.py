def benchmark(args):
    print('Batch size: {}'.format(args.batch_size))
    mf = ModelDownloader()
    init_net, pred_net, value_info = mf.get_c2_model(args.model)
    input_shapes = {k : [args.batch_size] + v[-1][1:] for (k, v) in value_info.items()}
    print("input info: {}".format(input_shapes))
    external_inputs = {}
    for k, v in input_shapes.items():
        external_inputs[k] = np.random.randn(*v).astype(np.float32)

    if args.device == 'CPU':
        device_option = core.DeviceOption(caffe2_pb2.CPU)
    elif args.device == 'MKL':
        device_option = core.DeviceOption(caffe2_pb2.MKLDNN)
    elif args.device == 'IDEEP':
        device_option = core.DeviceOption(caffe2_pb2.IDEEP)
    else:
        raise Exception("Unknown device: {}".format(args.device))
    print("Device option: {}, {}".format(args.device, device_option))
    pred_net.device_option.CopyFrom(device_option)
    for op in pred_net.op:
        op.device_option.CopyFrom(device_option)

    # Hack to initialized weights into MKL/IDEEP context
    workspace.RunNetOnce(init_net)
    bb = workspace.Blobs()
    weights = {}
    for b in bb:
        weights[b] = workspace.FetchBlob(b)
    for k, v in external_inputs.items():
        weights[k] = v
    workspace.ResetWorkspace()

    with core.DeviceScope(device_option):
        for name, blob in weights.items():
            #print("{}".format(name))
            workspace.FeedBlob(name, blob, device_option)
        workspace.CreateNet(pred_net)
        start = time.time()
        res = workspace.BenchmarkNet(pred_net.name,
                                     args.warmup_iterations,
                                     args.iterations,
                                     args.layer_wise_benchmark)
        print("FPS: {:.2f}".format(1/res[0]*1000*args.batch_size))
