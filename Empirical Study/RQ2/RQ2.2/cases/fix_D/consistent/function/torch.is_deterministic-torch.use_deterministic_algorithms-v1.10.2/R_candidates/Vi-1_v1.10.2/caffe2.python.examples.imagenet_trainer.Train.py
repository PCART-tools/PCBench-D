def Train(args):
    if args.model == "resnext":
        model_name = "resnext" + str(args.num_layers)
    elif args.model == "shufflenet":
        model_name = "shufflenet"

    # Either use specified device list or generate one
    if args.gpus is not None:
        gpus = [int(x) for x in args.gpus.split(',')]
        num_gpus = len(gpus)
    else:
        gpus = list(range(args.num_gpus))
        num_gpus = args.num_gpus

    log.info("Running on GPUs: {}".format(gpus))

    # Verify valid batch size
    total_batch_size = args.batch_size
    batch_per_device = total_batch_size // num_gpus
    assert \
        total_batch_size % num_gpus == 0, \
        "Number of GPUs must divide batch size"

    # Verify valid image mean/std per channel
    if args.image_mean_per_channel:
        assert \
            len(args.image_mean_per_channel) == args.num_channels, \
            "The number of channels of image mean doesn't match input"

    if args.image_std_per_channel:
        assert \
            len(args.image_std_per_channel) == args.num_channels, \
            "The number of channels of image std doesn't match input"

    # Round down epoch size to closest multiple of batch size across machines
    global_batch_size = total_batch_size * args.num_shards
    epoch_iters = int(args.epoch_size / global_batch_size)

    assert \
        epoch_iters > 0, \
        "Epoch size must be larger than batch size times shard count"

    args.epoch_size = epoch_iters * global_batch_size
    log.info("Using epoch size: {}".format(args.epoch_size))

    # Create ModelHelper object
    if args.use_ideep:
        train_arg_scope = {
            'use_cudnn': False,
            'cudnn_exhaustive_search': False,
            'training_mode': 1
        }
    else:
        train_arg_scope = {
            'order': 'NCHW',
            'use_cudnn': True,
            'cudnn_exhaustive_search': True,
            'ws_nbytes_limit': (args.cudnn_workspace_limit_mb * 1024 * 1024),
        }
    train_model = model_helper.ModelHelper(
        name=model_name, arg_scope=train_arg_scope
    )

    num_shards = args.num_shards
    shard_id = args.shard_id

    # Expect interfaces to be comma separated.
    # Use of multiple network interfaces is not yet complete,
    # so simply use the first one in the list.
    interfaces = args.distributed_interfaces.split(",")

    # Rendezvous using MPI when run with mpirun
    if os.getenv("OMPI_COMM_WORLD_SIZE") is not None:
        num_shards = int(os.getenv("OMPI_COMM_WORLD_SIZE", 1))
        shard_id = int(os.getenv("OMPI_COMM_WORLD_RANK", 0))
        if num_shards > 1:
            rendezvous = dict(
                kv_handler=None,
                num_shards=num_shards,
                shard_id=shard_id,
                engine="GLOO",
                transport=args.distributed_transport,
                interface=interfaces[0],
                mpi_rendezvous=True,
                exit_nets=None)

    elif num_shards > 1:
        # Create rendezvous for distributed computation
        store_handler = "store_handler"
        if args.redis_host is not None:
            # Use Redis for rendezvous if Redis host is specified
            workspace.RunOperatorOnce(
                core.CreateOperator(
                    "RedisStoreHandlerCreate", [], [store_handler],
                    host=args.redis_host,
                    port=args.redis_port,
                    prefix=args.run_id,
                )
            )
        else:
            # Use filesystem for rendezvous otherwise
            workspace.RunOperatorOnce(
                core.CreateOperator(
                    "FileStoreHandlerCreate", [], [store_handler],
                    path=args.file_store_path,
                    prefix=args.run_id,
                )
            )

        rendezvous = dict(
            kv_handler=store_handler,
            shard_id=shard_id,
            num_shards=num_shards,
            engine="GLOO",
            transport=args.distributed_transport,
            interface=interfaces[0],
            exit_nets=None)

    else:
        rendezvous = None

    # Model building functions
    def create_resnext_model_ops(model, loss_scale):
        initializer = (PseudoFP16Initializer if args.dtype == 'float16'
                       else Initializer)

        with brew.arg_scope([brew.conv, brew.fc],
                            WeightInitializer=initializer,
                            BiasInitializer=initializer,
                            enable_tensor_core=args.enable_tensor_core,
                            float16_compute=args.float16_compute):
            pred = resnet.create_resnext(
                model,
                "data",
                num_input_channels=args.num_channels,
                num_labels=args.num_labels,
                num_layers=args.num_layers,
                num_groups=args.resnext_num_groups,
                num_width_per_group=args.resnext_width_per_group,
                no_bias=True,
                no_loss=True,
            )

        if args.dtype == 'float16':
            pred = model.net.HalfToFloat(pred, pred + '_fp32')

        softmax, loss = model.SoftmaxWithLoss([pred, 'label'],
                                              ['softmax', 'loss'])
        loss = model.Scale(loss, scale=loss_scale)
        brew.accuracy(model, [softmax, "label"], "accuracy", top_k=1)
        brew.accuracy(model, [softmax, "label"], "accuracy_top5", top_k=5)
        return [loss]

    def create_shufflenet_model_ops(model, loss_scale):
        initializer = (PseudoFP16Initializer if args.dtype == 'float16'
                       else Initializer)

        with brew.arg_scope([brew.conv, brew.fc],
                            WeightInitializer=initializer,
                            BiasInitializer=initializer,
                            enable_tensor_core=args.enable_tensor_core,
                            float16_compute=args.float16_compute):
            pred = shufflenet.create_shufflenet(
                model,
                "data",
                num_input_channels=args.num_channels,
                num_labels=args.num_labels,
                no_loss=True,
            )

        if args.dtype == 'float16':
            pred = model.net.HalfToFloat(pred, pred + '_fp32')

        softmax, loss = model.SoftmaxWithLoss([pred, 'label'],
                                              ['softmax', 'loss'])
        loss = model.Scale(loss, scale=loss_scale)
        brew.accuracy(model, [softmax, "label"], "accuracy", top_k=1)
        brew.accuracy(model, [softmax, "label"], "accuracy_top5", top_k=5)
        return [loss]

    def add_optimizer(model):
        stepsz = int(30 * args.epoch_size / total_batch_size / num_shards)

        if args.float16_compute:
            # TODO: merge with multi-precision optimizer
            opt = optimizer.build_fp16_sgd(
                model,
                args.base_learning_rate,
                momentum=0.9,
                nesterov=1,
                weight_decay=args.weight_decay,   # weight decay included
                policy="step",
                stepsize=stepsz,
                gamma=0.1
            )
        else:
            optimizer.add_weight_decay(model, args.weight_decay)
            opt = optimizer.build_multi_precision_sgd(
                model,
                args.base_learning_rate,
                momentum=0.9,
                nesterov=1,
                policy="step",
                stepsize=stepsz,
                gamma=0.1
            )
        return opt

    # Define add_image_input function.
    # Depends on the "train_data" argument.
    # Note that the reader will be shared with between all GPUS.
    if args.train_data == "null":
        def add_image_input(model):
            AddNullInput(
                model,
                None,
                batch_size=batch_per_device,
                img_size=args.image_size,
                dtype=args.dtype,
            )
    else:
        reader = train_model.CreateDB(
            "reader",
            db=args.train_data,
            db_type=args.db_type,
            num_shards=num_shards,
            shard_id=shard_id,
        )

        def add_image_input(model):
            AddImageInput(
                model,
                reader,
                batch_size=batch_per_device,
                img_size=args.image_size,
                dtype=args.dtype,
                is_test=False,
                mean_per_channel=args.image_mean_per_channel,
                std_per_channel=args.image_std_per_channel,
            )

    def add_post_sync_ops(model):
        """Add ops applied after initial parameter sync."""
        for param_info in model.GetOptimizationParamInfo(model.GetParams()):
            if param_info.blob_copy is not None:
                model.param_init_net.HalfToFloat(
                    param_info.blob,
                    param_info.blob_copy[core.DataType.FLOAT]
                )

    data_parallel_model.Parallelize(
        train_model,
        input_builder_fun=add_image_input,
        forward_pass_builder_fun=create_resnext_model_ops
        if args.model == "resnext" else create_shufflenet_model_ops,
        optimizer_builder_fun=add_optimizer,
        post_sync_builder_fun=add_post_sync_ops,
        devices=gpus,
        rendezvous=rendezvous,
        optimize_gradient_memory=False,
        use_nccl=args.use_nccl,
        cpu_device=args.use_cpu,
        ideep=args.use_ideep,
        shared_model=args.use_cpu,
        combine_spatial_bn=args.use_cpu,
    )

    data_parallel_model.OptimizeGradientMemory(train_model, {}, set(), False)

    workspace.RunNetOnce(train_model.param_init_net)
    workspace.CreateNet(train_model.net)

    # Add test model, if specified
    test_model = None
    if (args.test_data is not None):
        log.info("----- Create test net ----")
        if args.use_ideep:
            test_arg_scope = {
                'use_cudnn': False,
                'cudnn_exhaustive_search': False,
            }
        else:
            test_arg_scope = {
                'order': "NCHW",
                'use_cudnn': True,
                'cudnn_exhaustive_search': True,
            }
        test_model = model_helper.ModelHelper(
            name=model_name + "_test",
            arg_scope=test_arg_scope,
            init_params=False,
        )

        test_reader = test_model.CreateDB(
            "test_reader",
            db=args.test_data,
            db_type=args.db_type,
        )

        def test_input_fn(model):
            AddImageInput(
                model,
                test_reader,
                batch_size=batch_per_device,
                img_size=args.image_size,
                dtype=args.dtype,
                is_test=True,
                mean_per_channel=args.image_mean_per_channel,
                std_per_channel=args.image_std_per_channel,
            )

        data_parallel_model.Parallelize(
            test_model,
            input_builder_fun=test_input_fn,
            forward_pass_builder_fun=create_resnext_model_ops
            if args.model == "resnext" else create_shufflenet_model_ops,
            post_sync_builder_fun=add_post_sync_ops,
            param_update_builder_fun=None,
            devices=gpus,
            use_nccl=args.use_nccl,
            cpu_device=args.use_cpu,
        )
        workspace.RunNetOnce(test_model.param_init_net)
        workspace.CreateNet(test_model.net)

    epoch = 0
    # load the pre-trained model and reset epoch
    if args.load_model_path is not None:
        LoadModel(args.load_model_path, train_model, args.use_ideep)

        # Sync the model params
        data_parallel_model.FinalizeAfterCheckpoint(train_model)

        # reset epoch. load_model_path should end with *_X.mdl,
        # where X is the epoch number
        last_str = args.load_model_path.split('_')[-1]
        if last_str.endswith('.mdl'):
            epoch = int(last_str[:-4])
            log.info("Reset epoch to {}".format(epoch))
        else:
            log.warning("The format of load_model_path doesn't match!")

    expname = "%s_gpu%d_b%d_L%d_lr%.2f_v2" % (
        model_name,
        args.num_gpus,
        total_batch_size,
        args.num_labels,
        args.base_learning_rate,
    )

    explog = experiment_util.ModelTrainerLog(expname, args)

    # Run the training one epoch a time
    while epoch < args.num_epochs:
        epoch = RunEpoch(
            args,
            epoch,
            train_model,
            test_model,
            total_batch_size,
            num_shards,
            expname,
            explog
        )

        # Save the model for each epoch
        SaveModel(args, train_model, epoch, args.use_ideep)

        model_path = "%s/%s_" % (
            args.file_store_path,
            args.save_model_name
        )
        # remove the saved model from the previous epoch if it exists
        if os.path.isfile(model_path + str(epoch - 1) + ".mdl"):
            os.remove(model_path + str(epoch - 1) + ".mdl")
