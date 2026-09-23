def _OptimizeGradientMemorySimple(model, losses_by_gpu, devices):
    log.warning("------- DEPRECATED API, please use " +
                   "data_parallel_model.OptimizeGradientMemory() ----- ")
    for device in devices:
        namescope = "{}_{}/".format(model._device_prefix, device)
        model.net._net = memonger.share_grad_blobs(
            model.net,
            losses_by_gpu[device],
            set(viewvalues(model.param_to_grad)),
            namescope,
            share_activations=False,
        )
