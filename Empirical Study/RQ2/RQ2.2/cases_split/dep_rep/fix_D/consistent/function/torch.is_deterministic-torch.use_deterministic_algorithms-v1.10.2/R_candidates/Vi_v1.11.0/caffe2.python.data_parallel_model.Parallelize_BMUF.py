def Parallelize_BMUF(
    model_helper_obj,
    input_builder_fun,
    forward_pass_builder_fun,
    param_update_builder_fun,
    block_learning_rate=1.0,
    block_momentum=None,
    devices=None,
    rendezvous=None,
    net_type='dag',
    master_device=None,
    use_nccl=False,
    nesterov=False,
    optimize_gradient_memory=False,
    reset_momentum_sgd=False,
    warmup_iterations=None,
    max_concurrent_distributed_ops=4,
    add_blobs_to_sync=None,
    num_threads_per_device=4,
    cpu_device=False,
    barrier_net_timeout_sec=_DEFAULT_BARRIER_NET_TIMEOUT_SEC,
):
    '''
    Function to create model that run on many GPUs and creates a net for
    parameter_updates that can be run independently for number of iterations
    then followed by another net that runs once to compute the final parameter
    updates according to block wise model update filtering rule described
    in : Scalable Training of Deep Learning Machines by Incremental Block
    Training with Intra-block Parallel Optimization and Blockwise Model-Update
    Filtering (ICASSP 2016).
    '''
    assert scope.CurrentDeviceScope() is None \
        or scope.CurrentDeviceScope().device_type == caffe2_pb2.CPU, \
        "Parallelize must be called without device-scope, \
        device scope was: {}".format(scope.CurrentDeviceScope())

    assert isinstance(model_helper_obj, model_helper.ModelHelper)

    if devices is None:
        devices = list(range(0, workspace.NumGpuDevices()))
    if master_device is None:
        master_device = devices[0]

    if not cpu_device:
        for gpu in devices:
            if gpu >= workspace.NumGpuDevices():
                log.warning("** Only {} GPUs available, GPUs {} requested".format(
                    workspace.NumGpuDevices(), devices))
                break
        model_helper_obj._device_type = workspace.GpuDeviceType
        model_helper_obj._device_prefix = "gpu"
    else:
        model_helper_obj._device_type = caffe2_pb2.CPU
        model_helper_obj._device_prefix = "cpu"

    model_helper_obj._devices = devices
    model_helper_obj._rendezvous = rendezvous
    model_helper_obj._sync_barrier_net = None
    model_helper_obj._broadcast_context = None
    model_helper_obj._shared_model = False
    master_dev_opt = core.DeviceOption(model_helper_obj._device_type, master_device)

    # question: rendezvous structure
    num_shards = rendezvous['num_shards'] if rendezvous else 1
    # num_devices is #devices across all machines
    num_devices = len(devices) * num_shards
    # num_workers is #threads to execute the DAG per shard
    num_workers = num_threads_per_device * len(devices)
    if rendezvous:
        num_workers += 8

    loss_scale = 1.0 / num_devices
    if block_momentum is None:
        block_momentum = 1.0 - 1.0 / num_devices

    max_concurrent_distributed_ops = min(
        max_concurrent_distributed_ops,
        num_workers - 1
    )

    model_helper_obj.net.Proto().num_workers = num_workers
    model_helper_obj.net.Proto().type = net_type

    # A net for initializing global model parameters. Its called once in the
    # same step as net parameters initialization.
    model_helper_obj._global_model_init_net = core.Net('global_model_init')
    model_helper_obj._global_model_init_net.Proto().type = net_type
    model_helper_obj._global_model_init_net.Proto().num_workers = \
        num_workers

    # A net for computing final parameter updates. Its will run once after
    # running net (local models updates) for `num_local_iterations` times.
    model_helper_obj._global_model_param_updates_net = core.Net('global_model')
    model_helper_obj._global_model_param_updates_net.Proto().type = net_type
    model_helper_obj._global_model_param_updates_net.Proto().num_workers = \
        num_workers

    def _v(param):
        return "{}_v".format(param)

    def _g(param):
        return "{}_g".format(param)

    def _v_prev(param):
        return "{}_prev".format(param)

    # Keep track of params that were in the model before: they are not
    # data parallel, so we need to handle them separately
    non_datapar_params = copy.copy(model_helper_obj.params)
    model_helper_obj._losses_by_gpu = {}

    def _InitializeModels(gpu_id):
        input_builder_fun(model_helper_obj)
        loss = forward_pass_builder_fun(model_helper_obj, loss_scale)
        model_helper_obj._losses_by_gpu[gpu_id] = loss
    _ForEachDevice(
        devices,
        _InitializeModels,
        device_type=model_helper_obj._device_type,
        device_prefix=model_helper_obj._device_prefix,
        scoped=True
    )
    _ValidateParams(model_helper_obj.params)

    model_helper_obj._device_grouped_blobs =\
        _GroupByDevice(model_helper_obj, devices,
                       model_helper_obj.params, non_datapar_params)

    model_helper_obj._param_names =\
        list(viewkeys(model_helper_obj._device_grouped_blobs))

    _AddGradientOperators(
        devices, model_helper_obj, model_helper_obj._losses_by_gpu
    )
    _ValidateParams(model_helper_obj.params)

    _InferBlobDevice(model_helper_obj)

    def _InitializeParamUpdate(gpu_id):
        param_update_builder_fun(model_helper_obj)
    _ForEachDevice(
        devices,
        _InitializeParamUpdate,
        device_type=model_helper_obj._device_type,
        device_prefix=model_helper_obj._device_prefix,
        scoped=True
    )

    model_parameter_names = list(
        viewkeys(model_helper_obj._device_grouped_blobs)
    )
    if warmup_iterations is not None:
        model_helper_obj._warmup_iterations = warmup_iterations
        # A net for broadcasting gpu-0 (master shard) parameters after
        # running net for `warmup_iterartions`.
        model_helper_obj._warmup_broadcast = core.Net('warmup-broadcast')
        model_helper_obj._warmup_broadcast.Proto().type = net_type
        model_helper_obj._warmup_broadcast.Proto().num_workers = \
           num_workers

        _SyncAllParams(
            devices,
            model_helper_obj,
            model_helper_obj.param_init_net,
            model_helper_obj._warmup_broadcast,
            rendezvous,
            model_parameter_names,
            max_concurrent_distributed_ops
        )
        for param_name in viewkeys(model_helper_obj._device_grouped_blobs):
            param = model_helper_obj._device_grouped_blobs[param_name][master_device]
            with core.DeviceScope(master_dev_opt):
                model_helper_obj._warmup_broadcast.Copy(param, _g(param))

    # (Step-0) Initialize momentum parameters on master device.
    for param_name in viewkeys(model_helper_obj._device_grouped_blobs):
        param = model_helper_obj._device_grouped_blobs[param_name][master_device]
        with core.DeviceScope(master_dev_opt):
            model_helper_obj._global_model_init_net.ConstantFill(
                param, _v(param), value=0.0
            )
            model_helper_obj._global_model_init_net.Copy(param, _g(param))
            if nesterov:
                model_helper_obj._global_model_init_net.ConstantFill(
                    param, _v_prev(param), value=0.0
                )

    # (Step-1) Update models for num_local_iterations.

    # (Step-2) Compute post-local-updates average of the params.
    # Sum model params across GPUs and store resutls in param_avg blob.
    _AllReduceBlobs(
        model_parameter_names,
        devices,
        model_helper_obj,
        model_helper_obj._global_model_param_updates_net,
        rendezvous,
        use_nccl,
        max_concurrent_distributed_ops
    )

    # (Step-3) Update momentum params :
    # param_v = block_momentum * param_v
    # + block_learning_Rate * (param_avg - param)
    # if nesterov momentum:
    # param = param + param_v
    # - block_momentum * (param_v - param_v_prev)
    # param_v_prev = param_v
    # else:
    # param = param + param_v
    for param_name in model_parameter_names:
        param = model_helper_obj._device_grouped_blobs[param_name][master_device]
        with core.DeviceScope(master_dev_opt):
            # TODO(ataei) : Stop building the graph here to get model average ?
            model_helper_obj._global_model_param_updates_net.Scale(
                param, param, scale=1.0 / num_devices
            )
            model_helper_obj._global_model_param_updates_net.Sub(
                [param, _g(param)], param
            )
            model_helper_obj._global_model_param_updates_net.Scale(
                param, param, scale=block_learning_rate
            )
            model_helper_obj._global_model_param_updates_net.Scale(
                _v(param), _v(param), scale=block_momentum
            )
            model_helper_obj._global_model_param_updates_net.Add(
                [_v(param), param], _v(param)
            )
            model_helper_obj._global_model_param_updates_net.Add(
                [_g(param), _v(param)], _g(param)
            )
            if nesterov:
                model_helper_obj._global_model_param_updates_net.Sub(
                    [_v(param), _v_prev(param)], _v_prev(param)
                )
                model_helper_obj._global_model_param_updates_net.Scale(
                    _v_prev(param), _v_prev(param), scale=block_momentum
                )
                model_helper_obj._global_model_param_updates_net.Sub(
                    [_g(param), _v_prev(param)], _g(param)
                )
                model_helper_obj._global_model_param_updates_net.Copy(
                    _v(param), _v_prev(param)
                )
            model_helper_obj._global_model_param_updates_net.Copy(
                _g(param), param
            )


    _SyncAllParams(
        devices,
        model_helper_obj,
        model_helper_obj.param_init_net,
        model_helper_obj._global_model_param_updates_net,
        rendezvous,
        model_parameter_names,
        max_concurrent_distributed_ops
    )

    # Add additional syncs
    if add_blobs_to_sync is not None:
        AddBlobSync(
            model_helper_obj,
            add_blobs_to_sync,
            net=model_helper_obj._global_model_param_updates_net)

    # Reset momentum-SGD parameters
    if reset_momentum_sgd:
        momentum_ops = [op for op in model_helper_obj.net.Proto().op
                        if op.type == 'MomentumSGDUpdate']
        for op in momentum_ops:
            momentum_blob = op.input[1]
            with core.DeviceScope(op.device_option):
                model_helper_obj._global_model_param_updates_net.ConstantFill(
                    [momentum_blob], momentum_blob, value=0.0
                )

    if optimize_gradient_memory:
        _OptimizeGradientMemorySimple(
            model_helper_obj, model_helper_obj._losses_by_gpu, devices
        )

    model_helper_obj._data_parallel_model_init_nets = [
        model_helper_obj.param_init_net,
        model_helper_obj._global_model_init_net
    ]

    model_helper_obj._data_parallel_model_nets = [
        model_helper_obj.net,
        (model_helper_obj._global_model_param_updates_net, 1)
    ]
    _AddBarrierToModelNets(model_helper_obj, barrier_net_timeout_sec)
