def OptimizeGradientMemory(model,
                           input_shapes,
                           excluded_blobs,
                           recycle_activations):
    """
    Optimize memory usage of the backward pass by recycling blobs for gradient
    inputs that have been 'used'.
    input_shapes:  dict of blob name to shape for the inputs of the model.
                   Pass empty dictionary if not known.
    excluded_blobs: list of blobs that cannot be recycled. These are blobs
                   that you will access externally.
    recycle_activations: whether to also recycle forward pass activations
    """
    if input_shapes is not None:
        input_shapes_all_devices = {}
        for b, shp in viewitems(input_shapes):
            for d in model._devices:
                input_shapes_all_devices["{}_{}/{}".
                                         format(model._device_prefix, d, b)] = shp

        (shapes, types) = workspace.InferShapesAndTypes(
            [model.param_init_net, model.net],
            input_shapes_all_devices,
        )
    else:
        shapes = None

    for device in model._devices:
        namescope = "{}_{}/".format(model._device_prefix, device)
        excluded_blobs_by_device = set(namescope + b for b in excluded_blobs)
        model.net._net = memonger.share_grad_blobs(
            model.net,
            model._losses_by_gpu[device],
            set(viewvalues(model.param_to_grad)),
            namescope,
            dont_share_blobs=excluded_blobs_by_device,
            share_activations=recycle_activations,
            blob_shapes=shapes,
        )
