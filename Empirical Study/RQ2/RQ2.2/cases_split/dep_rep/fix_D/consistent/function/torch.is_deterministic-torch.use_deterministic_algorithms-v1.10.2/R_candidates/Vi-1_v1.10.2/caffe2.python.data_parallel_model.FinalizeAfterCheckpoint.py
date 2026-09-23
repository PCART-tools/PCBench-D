def FinalizeAfterCheckpoint(model, blobs=None, cpu_mode=False):
    '''
    This function should be called after loading parameters from a
    checkpoint / initial parameters file.
    '''

    if not hasattr(model, "_checkpoint_net"):
        if blobs is None:
            (_, uniq_blob_names) = _ComputeBlobsToSync(model)
        else:
            uniq_blob_names = [stripBlobName(p) for p in blobs]

        # Synchronize to the blob lookup map, as the provided
        # blobs might have non-parameters, such as momentum blobs.
        log.info("Creating checkpoint synchronization net")
        devices = model.GetDevices()
        for name in uniq_blob_names:
            if name not in model._device_grouped_blobs:
                grouped = {
                    d:
                    core.BlobReference("{}_{}{}{}".format(
                        model._device_prefix,
                        d,
                        scope._NAMESCOPE_SEPARATOR,
                        name)
                    ) for d in devices}
                model._device_grouped_blobs[name] = grouped

        model._checkpoint_net = core.Net("checkpoint_sync_net")
        if not cpu_mode:
            model._checkpoint_net.RunAllOnGPU()

        checkpoint_init_net = None
        if (model._rendezvous is not None and model._rendezvous['num_shards'] > 1):
            checkpoint_init_net = core.Net("checkpoint_init_net")
            if not cpu_mode:
                checkpoint_init_net.RunAllOnGPU()

        _SyncAllParams(
            devices,
            model,
            checkpoint_init_net,
            model._checkpoint_net,
            model._rendezvous,
            uniq_blob_names,
            max_concurrent_distributed_ops=1
        )
        if (checkpoint_init_net):
            workspace.RunNetOnce(checkpoint_init_net)

        workspace.CreateNet(model._checkpoint_net)

    # Run the sync
    log.info("Run checkpoint net")
    workspace.RunNet(model._checkpoint_net.Proto().name)
