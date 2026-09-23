def AddBlobSync(model, blobs, net=None):
    '''
    Sync a blob across devices and hosts
    '''
    if len(blobs) == 0:
        return
    net = model.net if net is None else net
    for b in blobs:
        assert not b.startswith(model._device_prefix), \
            "Provide unprefixed blob name: {}".format(b)
        model._device_grouped_blobs[b] = {
            d: core.BlobReference("{}_{}/{}".format(model._device_prefix, d, b))
            for d in model._devices
        }

    _SyncAllParams(
        model._devices,
        model,
        model.param_init_net,
        net,
        model._rendezvous,
        set(blobs))
