def _AddDynamicMemoryOptimization(model, blobs_to_keep, devices):
    blobs_to_keep_all_devices = set()
    if blobs_to_keep is not None:
        for device in devices:
            for blob_name in blobs_to_keep:
                blobs_to_keep_all_devices.add(
                    "{}_{}/{}".format(model._device_prefix, device, blob_name)
                )

    if model._rendezvous is not None:
        # GLOO operators expect the tensor addresses to remain same over
        # iterations so we need to remove param grads from the dynamic memory
        # management.
        blobs_to_keep_all_devices.update(
            [str(b) for b in viewvalues(model.param_to_grad)]
        )

    model.net._net = memonger.release_blobs_when_used(
        model.net.Proto(),
        blobs_to_keep_all_devices
    )
