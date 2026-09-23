def build_resnet50_dataparallel_model(
        num_gpus,
        batch_size,
        epoch_size,
        cudnn_workspace_limit_mb=64,
        num_channels=3,
        num_labels=1000,
        weight_decay=1e-4,
        base_learning_rate=0.1,
        image_size=227,
        use_cpu=False):

    batch_per_device = batch_size // num_gpus

    train_arg_scope = {
        'order': 'NCHW',
        'use_cudnn': True,
        'cudnn_exhaustive_search': False,
        'ws_nbytes_limit': (cudnn_workspace_limit_mb * 1024 * 1024),
        'deterministic': True,
    }
    train_model = model_helper.ModelHelper(
        name="test_resnet50", arg_scope=train_arg_scope
    )

    def create_resnet50_model_ops(model, loss_scale):
        with brew.arg_scope([brew.conv, brew.fc],
                            WeightInitializer=Initializer,
                            BiasInitializer=Initializer,
                            enable_tensor_core=0):
            pred = resnet.create_resnet50(
                model,
                "data",
                num_input_channels=num_channels,
                num_labels=num_labels,
                no_bias=True,
                no_loss=True,
            )

        softmax, loss = model.SoftmaxWithLoss([pred, 'label'],
                                              ['softmax', 'loss'])
        loss = model.Scale(loss, scale=loss_scale)
        brew.accuracy(model, [softmax, "label"], "accuracy")
        return [loss]

    def add_optimizer(model):
        stepsz = int(30 * epoch_size / batch_size)
        optimizer.add_weight_decay(model, weight_decay)
        opt = optimizer.build_multi_precision_sgd(
            model,
            base_learning_rate,
            momentum=0.9,
            nesterov=1,
            policy="step",
            stepsize=stepsz,
            gamma=0.1
        )
        return opt

    def add_image_input(model):
        model.param_init_net.GaussianFill(
            [],
            ["data"],
            shape=[batch_per_device, 3, image_size, image_size],
            dtype='float',
        )
        model.param_init_net.ConstantFill(
            [],
            ["label"],
            shape=[batch_per_device],
            value=1,
            dtype=core.DataType.INT32,
        )

    def add_post_sync_ops(model):
        for param_info in model.GetOptimizationParamInfo(model.GetParams()):
            if param_info.blob_copy is not None:
                model.param_init_net.HalfToFloat(
                    param_info.blob,
                    param_info.blob_copy[core.DataType.FLOAT])

    # Create parallelized model
    data_parallel_model.Parallelize(
        train_model,
        input_builder_fun=add_image_input,
        forward_pass_builder_fun=create_resnet50_model_ops,
        optimizer_builder_fun=add_optimizer,
        post_sync_builder_fun=add_post_sync_ops,
        devices=list(range(num_gpus)),
        rendezvous=None,
        optimize_gradient_memory=True,
        cpu_device=use_cpu,
        shared_model=use_cpu,
    )

    return train_model
