def _GroupByDevice(model, devices, params, non_data_params):
    '''
    Groups blobs by device, returning a map of [blobname] = {0: BlobRef, 1: ..}.
    Returns ordered dictionary, ensuring the original order.
    '''
    grouped = OrderedDict()
    # Only consider params that were created to be  "data parallel"
    params = params[len(non_data_params):]

    for _i, p in enumerate(params):
        assert isinstance(p, core.BlobReference) or \
            isinstance(p, core.GradientSlice), \
            "Param {} is not BlobReference or GradientSlice".format(p)

        name = stripBlobName(p)
        gpuid = None

        if isinstance(p, core.BlobReference):
            gpuid = int(p.GetNameScope().split("_")[1].split("/")[0])
            assert "{}_{}/".format(model._device_prefix, gpuid) in p.GetNameScope(),\
                "Param {} expected to have namescope '{}_{}'".format(str(p), model._device_prefix, gpuid)
        else:
            gpuid = int(p.indices.GetNameScope().split("_")[1].split("/")[0])
            assert "{}_{}/".format(model._device_prefix, gpuid) in p.indices.GetNameScope(),\
                "Indices {} expected to have namescope '{}_{}'".format(str(p), model._device_prefix, gpuid)
            assert "{}_{}/".format(model._device_prefix, gpuid) in p.values.GetNameScope(),\
                "Values {} expected to have namescope '{}_{}'".format(str(p), model._device_prefix, gpuid)

        if name not in grouped:
            grouped[name] = {}
        grouped[name][gpuid] = p

    return grouped
