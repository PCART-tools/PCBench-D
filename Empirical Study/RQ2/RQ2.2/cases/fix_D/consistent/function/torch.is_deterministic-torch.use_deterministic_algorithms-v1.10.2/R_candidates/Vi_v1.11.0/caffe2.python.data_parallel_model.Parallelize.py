def Parallelize(
    model_helper_obj,
    input_builder_fun,
    forward_pass_builder_fun,
    param_update_builder_fun=None,
    optimizer_builder_fun=None,
    post_sync_builder_fun=None,
    pre_grad_net_transformer_fun=None,
    net_transformer_fun=None,
    devices=None,
    rendezvous=None,
    net_type='dag',
    broadcast_computed_params=True,
    optimize_gradient_memory=False,
    dynamic_memory_management=False,
    blobs_to_keep=None,
    use_nccl=False,
    max_concurrent_distributed_ops=16,
    cpu_device=False,
    ideep=False,
    num_threads_per_device=4,
    shared_model=False,
    combine_spatial_bn=False,
    barrier_net_timeout_sec=_DEFAULT_BARRIER_NET_TIMEOUT_SEC,
):
    '''
    Function to create a model that can run on many GPUs or CPUs.
      model_helper_obj: an object of ModelHelper
      input_builder_fun:
                         Function that adds the input operators
                         Note: Remember to instantiate reader outside of this
                         function so all devices share same reader object.
                         Signature:  input_builder_fun(model)
      forward_pass_builder_fun:
                        Function to add the operators to the model.
                        Must return list of loss-blob references that
                        are used to build the gradient. Loss scale parameter
                        is passed, as you should scale the loss of your model
                        by 1.0 / the total number of devices.
                        Signature: forward_pass_builder_fun(model, loss_scale)
      param_update_builder_fun:
                        Function that adds operators that are run after
                        gradient update, such as updating the weights and
                        weight decaying. This is called for each GPU separately.
                        Signature: param_update_builder_fun(model)
      optimizer_builder_fun:
                        Alternative to param_update_builder_fun, allows one
                        to add an optimizer for the whole model. Called only
                        once, without name or devicescope.
      net_transformer_fun:
                        Optional function to transform the network after the
                        network is built. It will be called once (NOT once per
                        GPU.)
                        Signature:
                        net_transformer_fun(
                            model, num_devices, device_prefix, device_type)
      pre_grad_net_transformer_fun:
                        Optional function to transform the network similar to
                        net_transformer_fun, but happens before gradient ops
                        been add.
                        Signature: pre_grad_net_transformer_fun(model)
      post_sync_builder_fun:
                        Function applied after initial parameter sync has been
                        completed, such as keeping multi-precision parameters
                        in sync.
                        Signature: post_sync_builder_fun(model)
      devices:          List of GPU ids, such as [0, 1, 2, 3],
      rendezvous:       used for rendezvous in distributed computation, if None
                        then only one node is used. To create rendezvous,
                        use <TBD>.
      net_type:         Network type
      optimize_gradient_memory: whether to apply 'memonger' to share blobs
      shared_model      (only for CPU) use same parameters on each device
                        in gradient computation to reduce memory footprint.
      dynamic_memory_management: Whether to apply dynamic memory optimization
                        by freeing unused blobs. The underlying (de)allocation
                        uses cached allocator. For GPU training PLEASE MAKE SURE
                        caffe2_cuda_memory_pool is set.
      blobs_to_keep :   A list of blob names to keep and don't free during
                        dynamic memory optimization (for example loss blob).
      cpu_device        Use CPU instead of GPU.
      ideep             Use ideep.
      combine_spatial_bn:
                        When set to True, applies batch normalization across
                        all devices within the node. If False, batch
                        normalization will be done separately for each device.
                        This option is currently only supported on the CPU.
      barrier_net_timeout_sec:
                        The timeout in seconds of the barrier net, which is run
                        to synchronize shards before a training epoch starts.
                        Defaults to 300 seconds.
    '''
    assert scope.CurrentDeviceScope() is None \
        or scope.CurrentDeviceScope().device_type == caffe2_pb2.CPU, \
        "Parallelize must be called without device-scope, \
        device scope was: {}".format(scope.CurrentDeviceScope())

    if devices is None:
        if not (cpu_device or ideep):
            devices = list(range(0, workspace.NumCudaDevices()))
        else:
            devices = list(range(0, cpu_count()))

    if not (cpu_device or ideep):
        for gpu in devices:
            if gpu >= workspace.NumGpuDevices():
                log.warning("** Only {} GPUs available, GPUs {} requested".format(
                    workspace.NumGpuDevices(), devices))
                break
        model_helper_obj._device_type = workspace.GpuDeviceType
        model_helper_obj._device_prefix = "gpu"
        model_helper_obj._shared_model = False
        device_name = "GPU"
        assert shared_model is False, "Shared model only supported on CPU"
    elif ideep:
        model_helper_obj._device_type = caffe2_pb2.IDEEP
        model_helper_obj._device_prefix = "ideep"
        device_name = "IDEEP"
        model_helper_obj._shared_model = shared_model
        if shared_model and rendezvous is not None:
            assert "Shared model only supported on single-node currently"
    else:
        model_helper_obj._device_type = caffe2_pb2.CPU
        model_helper_obj._device_prefix = "cpu"
        device_name = "CPU"
        model_helper_obj._shared_model = shared_model
        if shared_model and rendezvous is not None:
            assert "Shared model only supported on single-node currently"

    log.info("Parallelizing model for devices: {}".format(devices))
    extra_workers = 8 if rendezvous is not None else 0  # best-guess
    num_workers = len(devices) * num_threads_per_device + extra_workers
    max_concurrent_distributed_ops =\
        min(max_concurrent_distributed_ops, num_workers - 1)
    model_helper_obj.net.Proto().num_workers = num_workers
    model_helper_obj.net.Proto().type = net_type

    # Store some information in the model -- a bit ugly
    model_helper_obj._devices = devices
    model_helper_obj._rendezvous = rendezvous
    model_helper_obj._sync_barrier_net = None

    model_helper_obj._broadcast_context = None
    model_helper_obj._grad_names = []

    assert isinstance(model_helper_obj, model_helper.ModelHelper)

    # Keep track of params that were in the model before: they are not
    # data parallel, so we need to handle them separately
    non_datapar_params = copy.copy(model_helper_obj.params)

    # Add input and model
    log.info("Create input and model training operators")

    losses_by_gpu = {}
    num_shards = 1 if rendezvous is None else rendezvous['num_shards']
    loss_scale = 1.0 / (len(devices) * num_shards)

    has_parameter_updates = param_update_builder_fun is not None or \
        optimizer_builder_fun is not None
    assert not (
        param_update_builder_fun is not None and
        optimizer_builder_fun is not None
    ), 'Can only specify one of param_update_builder_fun, optimizer_builder_fun'

    # Check that a model that is used for validation/testing has
    # init_params False, otherwise running the param init net will overwrite
    # synchronized values by the training net
    if not has_parameter_updates and model_helper_obj.init_params:
        log.warning('')
        log.warning("############# WARNING #############")
        log.warning("Model {}/{} is used for testing/validation but".format(
            model_helper_obj.name, model_helper_obj))
        log.warning("has init_params=True!")
        log.warning("This can conflict with model training.")
        log.warning("Please ensure model = ModelHelper(init_params=False)")
        log.warning('####################################')
        log.warning('')
        # TODO: make into assert

    for device in devices:
        device_opt = core.DeviceOption(model_helper_obj._device_type, device)
        with core.DeviceScope(device_opt):
            with core.NameScope("{}_{}".format(model_helper_obj._device_prefix,
                                               device)):
                log.info("Model for {} : {}".format(device_name, device))
                input_builder_fun(model_helper_obj)
                losses = forward_pass_builder_fun(model_helper_obj, loss_scale)
                # Losses are not needed for test net
                if has_parameter_updates:
                    assert isinstance(losses, list), \
                        'Model builder function must return list of loss blobs'
                    for loss in losses:
                        assert isinstance(loss, core.BlobReference), \
                            'Model builder func must return list of loss blobs'

                losses_by_gpu[device] = losses
    _ValidateParams(model_helper_obj.params)

    # Create parameter map
    model_helper_obj._device_grouped_blobs =\
        _GroupByDevice(model_helper_obj, devices,
                       model_helper_obj.params, non_datapar_params)

    # computed params
    computed_params_grouped =\
        _GroupByDevice(model_helper_obj, devices,
                       model_helper_obj.GetComputedParams(''), [])
    model_helper_obj._device_grouped_blobs.update(computed_params_grouped)

    model_helper_obj._param_names =\
        list(viewkeys(model_helper_obj._device_grouped_blobs))
    model_helper_obj._computed_param_names =\
        list(viewkeys(computed_params_grouped))

    if pre_grad_net_transformer_fun:
        pre_grad_net_transformer_fun(model_helper_obj)

    if has_parameter_updates:
        log.info("Adding gradient operators")
        _AddGradientOperators(devices, model_helper_obj, losses_by_gpu)

    if net_transformer_fun:
        net_transformer_fun(
            model_helper_obj,
            len(devices),
            model_helper_obj._device_prefix,
            model_helper_obj._device_type)

    if not has_parameter_updates:
        log.info("Parameter update function not defined --> only forward")
        _InferBlobDevice(model_helper_obj)
        return

    if combine_spatial_bn:
        assert(has_parameter_updates), \
            'combine_spatial_bn should only be used for train model'
        _InterleaveOps(model_helper_obj)
        if cpu_device:
            _CPUInterDeviceBatchNormalization(model_helper_obj)
        else:
            _GPUInterDeviceBatchNormalization(model_helper_obj)

    _ValidateParams(model_helper_obj.params)

    # Group gradients by device and register to blob lookup
    param_to_grad = model_helper_obj.param_to_grad
    grads_ordered = [param_to_grad[p] for p in
                     model_helper_obj.params if p in param_to_grad]
    non_datapar_grads = [param_to_grad[p] for p in non_datapar_params]

    gradients_grouped = _GroupByDevice(
        model_helper_obj,
        devices,
        grads_ordered,
        non_datapar_grads
    )
    model_helper_obj._device_grouped_blobs.update(gradients_grouped)
    model_helper_obj._grad_names = list(viewkeys(gradients_grouped))
    model_helper_obj._losses_by_gpu = losses_by_gpu

    _InferBlobDevice(model_helper_obj)

    log.info("Add gradient all-reduces for SyncSGD")
    if broadcast_computed_params:
        _BroadcastComputedParams(devices, model_helper_obj, rendezvous, use_nccl)

    if len(model_helper_obj._grad_names) > 0:
        # Gradients in reverse order
        reverse_ordered_grads = _GetReverseOrderedGrads(model_helper_obj)
        assert(len(reverse_ordered_grads) > 0)
        _AllReduceBlobs(
            reverse_ordered_grads,
            devices,
            model_helper_obj,
            model_helper_obj.net,
            rendezvous,
            use_nccl,
            max_concurrent_distributed_ops,
        )
    else:
        log.info("NOTE: Param builder function did not create any parameters.")

    log.info("Post-iteration operators for updating params")
    num_shards = 1 if rendezvous is None else rendezvous['num_shards']

    all_params = set(model_helper_obj.GetParams(''))
    if shared_model:
        _PruneParametersForSharing(model_helper_obj)

    if param_update_builder_fun is not None:
        for device in devices:
            device_opt = core.DeviceOption(model_helper_obj._device_type, device)
            with core.DeviceScope(device_opt):
                with core.NameScope(
                    "{}_{}".format(model_helper_obj._device_prefix, device)
                ):
                    param_update_builder_fun(model_helper_obj)
    else:
        log.info("Calling optimizer builder function")
        optimizer = optimizer_builder_fun(model_helper_obj)
        model_helper_obj._optimizer = optimizer

    (sync_blobs, sync_names) = _ComputeBlobsToSync(model_helper_obj)
    sync_blobs_grouped = _GroupByDevice(
        model_helper_obj,
        devices,
        sync_blobs,
        [],
    )
    model_helper_obj._device_grouped_blobs.update(sync_blobs_grouped)

    _InferBlobDevice(model_helper_obj)
    _AnalyzeOperators(model_helper_obj)

    # Configure dagnet to run with only one worker on the first iteration,
    # to prevent concurrency problems with allocs and nccl.
    arg = model_helper_obj.Proto().arg.add()
    arg.name = "first_iter_only_one_worker"
    arg.i = 1

    # Add initial parameter syncs
    log.info("Add initial parameter sync")
    _SyncAllParams(
        devices,
        model_helper_obj,
        model_helper_obj.param_init_net,
        model_helper_obj.param_init_net,
        rendezvous,
        sync_names,
        max_concurrent_distributed_ops=1
    )

    # Handle any operations that need to be done after parameter sync
    # i.e. making sure multi-precision copies of parameters are up-to-date
    if post_sync_builder_fun is not None:
        for device in devices:
            device_opt = core.DeviceOption(model_helper_obj._device_type, device)
            with core.DeviceScope(device_opt):
                with core.NameScope(
                    "{}_{}".format(model_helper_obj._device_prefix, device)
                ):
                    post_sync_builder_fun(model_helper_obj)

    assert not (optimize_gradient_memory and dynamic_memory_management), \
        """It is not advised to use gradient optimization ('memonger')
        with dynamic memory management."""

    if optimize_gradient_memory:
        _OptimizeGradientMemorySimple(model_helper_obj, losses_by_gpu, devices)

    if dynamic_memory_management:
        _AddDynamicMemoryOptimization(model_helper_obj, blobs_to_keep, devices)


    model_helper_obj._data_parallel_model_init_nets = [
        model_helper_obj.param_init_net,
    ]

    model_helper_obj._data_parallel_model_nets = [
        model_helper_obj.net
    ]
    _AddBarrierToModelNets(model_helper_obj, barrier_net_timeout_sec)

    if shared_model:
        _RemapParameterBlobsForSharedModel(model_helper_obj, all_params)
