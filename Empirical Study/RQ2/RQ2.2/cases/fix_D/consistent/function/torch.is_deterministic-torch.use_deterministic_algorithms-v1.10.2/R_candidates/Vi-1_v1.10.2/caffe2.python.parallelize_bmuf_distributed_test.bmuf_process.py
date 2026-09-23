def bmuf_process(filestore_dir, process_id, shared_results,
                 cpu_device=False, nesterov=False):
    # We need to import caffe2 in every process to initialize CUDA independently.
    from caffe2.python import core, cnn, data_parallel_model, dyndep
    from caffe2.proto import caffe2_pb2
    dyndep.InitOpsLibrary("@/caffe2/caffe2/distributed:file_store_handler_ops")

    if not cpu_device:
        if not workspace.has_gpu_support:
            log.info('No GPU support test is Ignored.')
            return
        if workspace.NumGpuDevices() < 4:
            log.info('Not enough GPU support, test IGNORED')
            return

    model = cnn.CNNModelHelper(
        order="NHWC",
        name="test"
    )
    if not cpu_device:
        device_type = workspace.GpuDeviceType
        device_prefix = "gpu"
    else:
        device_type = caffe2_pb2.CPU
        device_prefix = "cpu"

    devices = [0, 1] if process_id == 0 else [2, 3]

    def _model_build_fun(model, loss_scale):
        fc = model.FC(
            "data", "fc", 16, 1, ("ConstantFill", {}), ("ConstantFill", {})
        )
        fc_fl = model.FlattenToVec(fc, "fc_fl")
        sigm = model.Sigmoid(fc_fl, "sigm")
        sq = model.SquaredL2Distance([sigm, "label"], "sq")
        loss = model.AveragedLoss(sq, "loss")
        loss = model.Scale(loss, scale=loss_scale)

        # For testing explicit sync
        model.param_init_net.UniformFill([], ["sync_num"], shape=[1])
        return [loss]

    def _input_builder_fun(model):
        return None

    def _param_update_fun(model):
        ITER = model.Iter("ITER")
        LR = model.net.LearningRate(
            [ITER],
            "LR",
            base_lr=(-0.1),
            policy="fixed",
        )
        ONE = model.param_init_net.ConstantFill(
            [], "ONE", shape=[1], value=1.0,
        )
        for param in model.GetParams():
            grad = model.param_to_grad[param]
            model.WeightedSum([param, ONE, grad, LR], param)

    def _generate_data(devices, process_id, device_type, device_prefix):
        np.random.seed(26 + process_id * 10)
        # Each run has same input, independent of number of gpus
        batch_size = 64
        for _ in range(0, 10):
            full_data = np.random.rand(batch_size, 16)
            full_labels = np.round(full_data[:, 0])
            batch_per_device = batch_size // len(devices)

            for (j, g) in enumerate(devices):
                st = j * batch_per_device
                en = st + batch_per_device
                data = full_data[st:en, :].astype(np.float32)
                labels = full_labels[st:en].astype(np.float32)
                with core.DeviceScope(core.DeviceOption(device_type, g)):
                    workspace.FeedBlob("{}_{}/data".format(device_prefix, g), data)
                    workspace.FeedBlob("{}_{}/label".format(device_prefix, g), labels)

    _generate_data(devices, process_id, device_type, device_prefix)

    workspace.RunOperatorOnce(
        core.CreateOperator(
            "FileStoreHandlerCreate", [], ["store_handler"],
            path=filestore_dir
        )
    )
    rendezvous = dict(
        kv_handler="store_handler",
        shard_id=process_id,
        num_shards=2,
        engine="GLOO",
        exit_nets=None
    )

    data_parallel_model.Parallelize_BMUF(
        model,
        _input_builder_fun,
        _model_build_fun,
        _param_update_fun,
        devices=devices,
        rendezvous=rendezvous,
        nesterov=nesterov,
        add_blobs_to_sync=["sync_num"],
        cpu_device=cpu_device
    )

    data_parallel_model.RunInitNet(model)

    def _device_pid(device, pid):
        if pid == 1:
            return device + 2
        return device

    np.testing.assert_equal(
        workspace.FetchBlob("{}_{}/fc_w_v".format(
            device_prefix, _device_pid(0, process_id))),
        np.zeros(16).astype(np.float32).reshape(1, 16)
    )

    # Run the algorithm for one iteration to have non-zero params.
    data_parallel_model.RunNet(model, 1)

    # Save iteration momentum and post local update params
    results = {}
    v_b_ = workspace.FetchBlob(
        "{}_{}/fc_b_v".format(device_prefix, _device_pid(0, process_id)))
    v_w_ = workspace.FetchBlob(
        "{}_{}/fc_w_v".format(device_prefix, _device_pid(0, process_id)))

    results['v_b_'] = v_b_
    results['v_w_'] = v_w_

    workspace.RunNetOnce(model.net)

    b_0_ = workspace.FetchBlob(
        "{}_{}/fc_b".format(device_prefix, _device_pid(0, process_id)))
    w_0_ = workspace.FetchBlob(
        "{}_{}/fc_w".format(device_prefix, _device_pid(0, process_id)))
    b_1_ = workspace.FetchBlob(
        "{}_{}/fc_b".format(device_prefix, _device_pid(1, process_id)))
    w_1_ = workspace.FetchBlob(
        "{}_{}/fc_w".format(device_prefix, _device_pid(1, process_id)))

    results['b_0_'] = b_0_
    results['w_0_'] = w_0_
    results['b_1_'] = b_1_
    results['w_1_'] = w_1_

    # Test sync
    if process_id == 0:
        workspace.FeedBlob(
            device_prefix + "_0/sync_num",
            np.array([2603]).astype(np.float32),
            device_option=core.DeviceOption(device_type, 0))

    # Compute block gradients.
    b_g_ = workspace.FetchBlob(
        "{}_{}/fc_b_g".format(device_prefix, _device_pid(0, process_id)))
    w_g_ = workspace.FetchBlob(
        "{}_{}/fc_w_g".format(device_prefix, _device_pid(0, process_id)))
    results['b_g_'] = b_g_
    results['w_g_'] = w_g_
    workspace.RunNetOnce(model._global_model_param_updates_net)

    #  g_b = (b_0_ + b_1_) / 2 - b_g_
    #  g_w = (w_0_ + w_1_) / 2 - w_g_
    v_b = workspace.FetchBlob(
        "{}_{}/fc_b_v".format(device_prefix, _device_pid(0, process_id)))
    v_w = workspace.FetchBlob(
        "{}_{}/fc_w_v".format(device_prefix, _device_pid(0, process_id)))
    w_g = workspace.FetchBlob(
        "{}_{}/fc_w_g".format(device_prefix, _device_pid(0, process_id)))
    b_g = workspace.FetchBlob(
        "{}_{}/fc_b_g".format(device_prefix, _device_pid(0, process_id)))
    w_0 = workspace.FetchBlob(
        "{}_{}/fc_w".format(device_prefix, _device_pid(0, process_id)))
    b_0 = workspace.FetchBlob(
        "{}_{}/fc_b".format(device_prefix, _device_pid(0, process_id)))
    w_1 = workspace.FetchBlob(
        "{}_{}/fc_w".format(device_prefix, _device_pid(1, process_id)))
    b_1 = workspace.FetchBlob(
        "{}_{}/fc_b".format(device_prefix, _device_pid(1, process_id)))
    results['v_b'] = v_b
    results['v_w'] = v_w
    results['w_g'] = w_g
    results['b_g'] = b_g
    results['w_0'] = w_0
    results['b_0'] = b_0
    results['w_1'] = w_1
    results['b_1'] = b_1

    # Test add_blobs_to_sync
    for j in devices:
        sync = workspace.FetchBlob(
            device_prefix + "_{}/sync_num".format(j))[0]
        results['sync_{}'.format(j)] = sync

    shared_results[process_id] = results
