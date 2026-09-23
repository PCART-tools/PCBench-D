def _Broadcast(devices, model, net, param, use_nccl=False):
    # Copy params from gpu_0 to other
    master_dev = devices[0]

    if use_nccl:
        if _IsGPUBlob(model, param):
            master_device_opt = core.DeviceOption(model._device_type, master_dev)
            with core.DeviceScope(master_device_opt):
                # Note that the root is the root _rank_ and not the root
                # _device_. Thus we always use root=0, regardless of the
                # devices used.
                net.NCCLBroadcast(
                    list(viewvalues(model._device_grouped_blobs[param])),
                    list(viewvalues(model._device_grouped_blobs[param])),
                    root=0,
                )
                return

    for dev_idx in devices[1:]:
        if _IsGPUBlob(model, param):
            device_opt = core.DeviceOption(workspace.GpuDeviceType, dev_idx)
        else:
            device_opt = core.DeviceOption(caffe2_pb2.IDEEP, 0) if _IsIDEEPBlob(model, param) else \
                core.DeviceOption(caffe2_pb2.CPU, 0)
        with core.DeviceScope(device_opt):
            net.Copy(
                model._device_grouped_blobs[param][master_dev],
                model._device_grouped_blobs[param][dev_idx]
            )
