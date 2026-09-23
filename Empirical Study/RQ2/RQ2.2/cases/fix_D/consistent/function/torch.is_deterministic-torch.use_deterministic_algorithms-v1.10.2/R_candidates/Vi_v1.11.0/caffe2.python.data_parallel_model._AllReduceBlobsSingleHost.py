def _AllReduceBlobsSingleHost(blob_names, devices, model, net, use_nccl):
    """Performs NCCL AllReduce to distribute blobs to all the GPUs."""

    if len(devices) == 1:
        return

    # Now we need to Allreduce blobs on all the GPUs.
    # Pick GPU #0 as a master GPU.
    master_device_opt = core.DeviceOption(model._device_type, devices[0])
    last_out = None
    concatenated_idx = set()

    for blob_name in blob_names:
        # Group by blob_name for reduce.
        blobs_group = list(viewvalues(model._device_grouped_blobs[blob_name]))
        if len(blobs_group) == 1:
            # Non-reducible
            continue
        assert len(blobs_group) == len(devices), \
            "Each GPU from {}, should have a copy of {}.".format(
                devices, blob_name)

        if _IsGPUBlob(model, blob_name):
            with core.DeviceScope(master_device_opt):
                if not isinstance(blobs_group[0], core.GradientSlice):
                    _AllReduce(
                        devices, model, net, blob_name, use_nccl, last_out
                    )
                    # last_out is used to serialize the execution of nccls
                    last_out = blobs_group[0]

                else:
                    # Sparse gradients: all-gather for indices and values
                    master_ns = "{}_{}".format(model._device_prefix, devices[0])
                    '''
                    Skip if we have already copied concatenated indices
                    to the indices of GradientSlice. This happens when two
                    or more grad blobs are gathered with the same indices
                    blob
                    '''
                    skip_idx_concat = False
                    for g in blobs_group:
                        if g.indices in concatenated_idx:
                            skip_idx_concat = True

                    if not skip_idx_concat:
                        grad_idx_concat, _ = net.Concat(
                            [g.indices for g in blobs_group],
                            ["{}/{}_index_concat".format(master_ns, blob_name),
                             "{}/{}_index_splitinfo".format(master_ns, blob_name)],
                            axis=0,
                            name="note:data_parallel_model")

                        for gpu, g in viewitems(model._device_grouped_blobs[blob_name]):
                            device_opt = core.DeviceOption(model._device_type, gpu)
                            with core.DeviceScope(device_opt):
                                model.Copy(grad_idx_concat, g.indices)
                                concatenated_idx.add(g.indices)

                    grad_val_concat, _ = net.Concat(
                        [g.values for g in blobs_group],
                        ["{}/{}_val_concat".format(master_ns, blob_name),
                         "{}/{}_val_splitinfo".format(master_ns, blob_name)],
                        axis=0, name="note:data_parallel_model")

                    for gpu, g in viewitems(model._device_grouped_blobs[blob_name]):
                        device_opt = core.DeviceOption(model._device_type, gpu)
                        with core.DeviceScope(device_opt):
                            model.Copy(grad_val_concat, g.values)

        elif _IsIDEEPBlob(model, blob_name):
            assert not isinstance(blobs_group[0], core.GradientSlice), \
                "Synchronizing gradient slices not supported"
            with core.DeviceScope(core.DeviceOption(caffe2_pb2.IDEEP)):
                net.Sum(blobs_group, [blobs_group[0]])
                if not model._shared_model:
                    _Broadcast(devices, model, net, blob_name)

        else:
            assert not isinstance(blobs_group[0], core.GradientSlice), \
                "Synchronizing gradient slices not supported"
            with core.DeviceScope(core.DeviceOption(caffe2_pb2.CPU)):
                # Poor man's allreduce
                net.Sum(blobs_group, [blobs_group[0]])
                if not model._shared_model:
                    _Broadcast(devices, model, net, blob_name)
