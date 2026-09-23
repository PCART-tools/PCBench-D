def Optimize(args):
    init_net = caffe2_pb2.NetDef()
    predict_net = caffe2_pb2.NetDef()
    init_net.ParseFromString(args.init_net.read())
    predict_net.ParseFromString(args.pred_net.read())

    workspace.ResetWorkspace()
    workspace.RunNetOnce(init_net)
    param_dict = {p: workspace.FetchBlob(p) for p in workspace.Blobs()}

    external_inputs = {}
    external_outputs = {}
    if args.verify_input:
        value_info = json.load(args.verify_input)
        input_shapes = {k : v[-1] for (k, v) in value_info.items()}
        print("input info: {}".format(input_shapes))
        for k, v in input_shapes.items():
            external_inputs[k] = np.random.randn(*v).astype(np.float32)
            workspace.FeedBlob(k, external_inputs[k])
        workspace.RunNetOnce(predict_net)
        for o in predict_net.external_output:
            external_outputs[o] = workspace.FetchBlob(o)

    if args.fuse_mul_add:
        predict_net, param_dict, _ = fuse_mul_add(predict_net, param_dict)
    if args.fuse_bn:
        predict_net, param_dict, _ = fuse_bn(predict_net, param_dict, False)
    if args.fuse_conv_relu:
        predict_net = fuse_conv_relu(predict_net)

    external_outputs_opt = {}
    if args.verify_input:
        workspace.ResetWorkspace()
        device_option = core.DeviceOption(caffe2_pb2.IDEEP) if args.fuse_conv_relu else core.DeviceOption(caffe2_pb2.CPU)
        with core.DeviceScope(device_option):
            for k, v in param_dict.items():
                workspace.FeedBlob(k, v, device_option)
            for k, v in external_inputs.items():
                workspace.FeedBlob(k, v, device_option)
            workspace.RunNetOnce(predict_net)
            for o in predict_net.external_output:
                external_outputs_opt[o] = workspace.FetchBlob(o)
                assert np.allclose(external_outputs[o],
                                   external_outputs_opt[o],
                                   atol=1e-3,
                                   rtol=1e-3)

    for i, o in enumerate(predict_net.op):
        print("op[{}]: {}".format(i, o.type))
    init_net = gen_init_net_from_blobs(param_dict)
    with open('init_net.pb', 'wb') as f:
        f.write(init_net.SerializeToString())
    with open('predict_net.pb', 'wb') as f:
        f.write(predict_net.SerializeToString())
