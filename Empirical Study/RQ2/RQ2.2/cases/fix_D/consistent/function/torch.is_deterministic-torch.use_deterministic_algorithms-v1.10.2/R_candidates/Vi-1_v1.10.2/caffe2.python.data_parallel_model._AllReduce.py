def _AllReduce(devices, model, net, param, use_nccl=False, control_input=None):
    blobs_group = list(viewvalues(model._device_grouped_blobs[param]))
    if model._device_type == caffe2_pb2.CUDA and use_nccl:
        # TODO: for _shared_model, do only NCCLReduce
        model.NCCLAllreduce(
            blobs_group, blobs_group, control_input=control_input
        )
        return

    if model._device_type == workspace.GpuDeviceType:
        p2p_access_pattern = workspace.GetGpuPeerAccessPattern()
    else:
        p2p_access_pattern = None

    def sumN(*dev_indices):
        """Create a Sum op for 2 or more blobs on different devices.
        Saves the result on the first device.

        Args:
        dev_indices -- a list of device indices, which can be translated into
                       CUDA identifiers with model._devices
        """
        devices = [model._devices[idx] for idx in dev_indices]
        blobs = [blobs_group[idx] for idx in dev_indices]
        device_opt = core.DeviceOption(model._device_type, devices[0])
        with core.DeviceScope(device_opt):
            for i, peer in enumerate(devices):
                if i == 0:
                    continue  # Skip the first device
                if p2p_access_pattern is not None and p2p_access_pattern.size and not p2p_access_pattern[
                    devices[0], peer
                ]:
                    # Copy from peer to d0
                    blobs[i] = model.Copy(
                        blobs[i],
                        'gpu_{}/{}_gpu{}_copy'.format(devices[0], param, peer)
                    )
            net.Sum(blobs, [blobs[0]], name='dpm')

    if len(devices) == 16:
        # Special tree reduction for 16 gpus, TODO generalize like in muji.py
        for j in range(8):
            sumN(j * 2, j * 2 + 1)
        for j in range(4):
            sumN(j * 4, j * 4 + 2)
        for j in range(2):
            sumN(j * 8, j * 8 + 4)
        sumN(0, 8)
    elif len(devices) == 8:
        for j in range(4):
            sumN(j * 2, j * 2 + 1)
        for j in range(2):
            sumN(j * 4, j * 4 + 2)
        sumN(0, 4)
    elif len(devices) == 4:
        sumN(0, 1)
        sumN(2, 3)
        sumN(0, 2)
    else:
        sumN(*range(len(devices)))
    # TODO: for _shared_model, no need to broadcast
    _Broadcast(devices, model, net, param)
