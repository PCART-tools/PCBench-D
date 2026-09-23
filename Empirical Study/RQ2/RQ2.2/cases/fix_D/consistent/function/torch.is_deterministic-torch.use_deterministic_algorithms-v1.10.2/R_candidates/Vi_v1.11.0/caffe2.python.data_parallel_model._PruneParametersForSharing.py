def _PruneParametersForSharing(model):
    assert model._shared_model
    master_prefix = "{}_{}/".format(model._device_prefix, model._devices[0])

    # Remove non-master parameters so that they will not receive parameter
    # update operators.
    model.params = model.GetParams(master_prefix)
    paramset = set(model.params)

    model.param_to_grad = {
        p: model.param_to_grad[p]
        for p in model.param_to_grad if p in paramset
    }
    model.weights = [w for w in model.weights if w in paramset]
    model.biases = [w for w in model.biases if w in paramset]
