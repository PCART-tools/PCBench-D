def LoadModel(path, model, use_ideep):
    '''
    Load pretrained model from file
    '''
    log.info("Loading path: {}".format(path))
    meta_net_def = pred_exp.load_from_db(path, 'minidb')
    init_net = core.Net(pred_utils.GetNet(
        meta_net_def, predictor_constants.GLOBAL_INIT_NET_TYPE))
    predict_init_net = core.Net(pred_utils.GetNet(
        meta_net_def, predictor_constants.PREDICT_INIT_NET_TYPE))

    if use_ideep:
        predict_init_net.RunAllOnIDEEP()
    else:
        predict_init_net.RunAllOnGPU()
    if use_ideep:
        init_net.RunAllOnIDEEP()
    else:
        init_net.RunAllOnGPU()

    assert workspace.RunNetOnce(predict_init_net)
    assert workspace.RunNetOnce(init_net)

    # Hack: fix iteration counter which is in CUDA context after load model
    itercnt = workspace.FetchBlob("optimizer_iteration")
    workspace.FeedBlob(
        "optimizer_iteration",
        itercnt,
        device_option=core.DeviceOption(caffe2_pb2.CPU, 0)
    )
