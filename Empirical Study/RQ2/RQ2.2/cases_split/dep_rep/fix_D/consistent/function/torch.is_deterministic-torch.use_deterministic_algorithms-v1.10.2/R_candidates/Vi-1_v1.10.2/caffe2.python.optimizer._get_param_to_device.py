def _get_param_to_device(model):
    # Infer blob devices by going through the net and param_init_net
    # ops and observing the device used to create or use the blob.
    param_to_device = core.InferBlobDevices(model.net)
    param_to_device.update(core.InferBlobDevices(model.param_init_net))
    return param_to_device
