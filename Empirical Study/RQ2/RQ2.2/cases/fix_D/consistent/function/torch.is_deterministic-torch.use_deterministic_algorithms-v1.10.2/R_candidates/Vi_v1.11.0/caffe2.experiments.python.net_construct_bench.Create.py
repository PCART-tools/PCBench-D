def Create(args):
    gpus = list(range(args.num_gpus))
    log.info("Running on gpus: {}".format(gpus))

    # Create CNNModeLhelper object
    train_model = cnn.CNNModelHelper(
        order="NCHW",
        name="resnet50",
        use_cudnn=True,
        cudnn_exhaustive_search=False
    )

    # Model building functions
    def create_resnet50_model_ops(model, loss_scale):
        [softmax, loss] = resnet.create_resnet50(
            model,
            "data",
            num_input_channels=3,
            num_labels=1000,
            label="label",
        )
        model.Accuracy([softmax, "label"], "accuracy")
        return [loss]

    # SGD
    def add_parameter_update_ops(model):
        model.AddWeightDecay(1e-4)
        ITER = model.Iter("ITER")
        stepsz = int(30)
        LR = model.net.LearningRate(
            [ITER],
            "LR",
            base_lr=0.1,
            policy="step",
            stepsize=stepsz,
            gamma=0.1,
        )
        AddMomentumParameterUpdate(model, LR)

    def add_image_input(model):
        pass

    start_time = time.time()

    # Create parallelized model
    data_parallel_model.Parallelize_GPU(
        train_model,
        input_builder_fun=add_image_input,
        forward_pass_builder_fun=create_resnet50_model_ops,
        param_update_builder_fun=add_parameter_update_ops,
        devices=gpus,
    )

    ct = time.time() - start_time
    train_model.net._CheckLookupTables()

    log.info("Model create for {} gpus took: {} secs".format(len(gpus), ct))
