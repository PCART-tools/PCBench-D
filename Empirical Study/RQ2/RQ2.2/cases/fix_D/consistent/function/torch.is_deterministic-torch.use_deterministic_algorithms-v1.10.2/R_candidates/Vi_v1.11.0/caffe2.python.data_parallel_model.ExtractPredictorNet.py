def ExtractPredictorNet(model, inputs, outputs, device):
    '''
    Returns (net, params) that can be exported to be used as a prediction
    net.
    '''
    master_device = model._devices[0]
    prefix = "{}_{}/".format(model._device_prefix, master_device)
    prefix_inputs = [prefix + str(b) for b in inputs]
    prefix_outputs = [prefix + str(b) for b in outputs]
    (predictor_net, export_blobs) = model_helper.ExtractPredictorNet(
        net_proto=model.net.Proto(),
        input_blobs=prefix_inputs,
        output_blobs=prefix_outputs,
        device=device,
        renames={
            a: b
            for (a, b) in zip(prefix_inputs + prefix_outputs, inputs + outputs)
        },
    )

    return (predictor_net, export_blobs)
