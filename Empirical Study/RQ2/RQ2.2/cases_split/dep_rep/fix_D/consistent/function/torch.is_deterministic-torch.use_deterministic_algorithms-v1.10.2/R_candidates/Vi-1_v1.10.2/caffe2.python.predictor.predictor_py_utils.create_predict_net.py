def create_predict_net(predictor_export_meta):
    """
    Return the input prediction net.
    """
    # Construct a new net to clear the existing settings.
    net = core.Net(predictor_export_meta.predict_net.name or "predict")
    net.Proto().op.extend(predictor_export_meta.predict_net.op)
    net.Proto().partition_info.extend(predictor_export_meta.predict_net.partition_info)
    net.Proto().external_input.extend(
        predictor_export_meta.inputs + predictor_export_meta.parameters
    )
    net.Proto().external_output.extend(predictor_export_meta.outputs)
    net.Proto().arg.extend(predictor_export_meta.predict_net.arg)
    if predictor_export_meta.net_type is not None:
        net.Proto().type = predictor_export_meta.net_type
    if predictor_export_meta.num_workers is not None:
        net.Proto().num_workers = predictor_export_meta.num_workers
    return net.Proto()
