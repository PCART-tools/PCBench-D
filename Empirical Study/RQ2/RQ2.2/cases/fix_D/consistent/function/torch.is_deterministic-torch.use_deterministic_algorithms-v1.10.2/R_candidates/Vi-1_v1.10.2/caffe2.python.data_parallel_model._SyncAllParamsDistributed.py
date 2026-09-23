def _SyncAllParamsDistributed(
    devices,
    model,
    init_net,
    net,
    rendezvous,
    unique_param_names,
    max_concurrent_distributed_ops
):
    assert rendezvous['num_shards'] > 1

    gpu_device_opt = core.DeviceOption(model._device_type, devices[0])
    cpu_device_opt = core.DeviceOption(caffe2_pb2.CPU)
    ideep_device_opt = core.DeviceOption(caffe2_pb2.IDEEP)

    if model._broadcast_context is None:
        model._broadcast_context = CollectivesConcurrencyControl(
            "broadcast",
            max_concurrent_distributed_ops,
            init_net,
            rendezvous
        )
    context = model._broadcast_context

    for param_name in sorted(unique_param_names):
        master_param = model._device_grouped_blobs[param_name][devices[0]]
        params_group = list(viewvalues(model._device_grouped_blobs[param_name]))

        def broadcast(params):
            comm_world, control_input = context.get_control_and_context(params)
            net.Broadcast(
                inputs=[comm_world] + params,
                outputs=params,
                name=param_name,
                engine=rendezvous['engine'],
                control_input=control_input
            )

        device_opt = gpu_device_opt if _IsGPUBlob(
            model, param_name
        ) else ideep_device_opt if _IsIDEEPBlob(model, param_name) else cpu_device_opt

        if rendezvous['engine'] == 'GLOO':
            with core.DeviceScope(device_opt):
                broadcast(params_group)
        else:
            # Copy between GPU and CPU
            with core.DeviceScope(device_opt):
                param_cpu = net.CopyGPUToCPU(
                    master_param,
                    str(master_param) + "cpu"
                )
            with core.DeviceScope(cpu_device_opt):
                broadcast([param_cpu])
            with core.DeviceScope(device_opt):
                net.CopyCPUToGPU(param_cpu, master_param)

            # Broadcast locally
            _Broadcast(devices, model, net, param_name)
