def _global_init_net(predictor_export_meta, db_type):
    net = core.Net("global-init")
    # manifold_db does not need DBReader
    if db_type != "manifold_db":
        net.Load(
            [predictor_constants.PREDICTOR_DBREADER],
            predictor_export_meta.parameters)
        net.Proto().external_input.extend([predictor_constants.PREDICTOR_DBREADER])
        net.Proto().external_output.extend(predictor_export_meta.parameters)

    if predictor_export_meta.global_init_net:
        net.AppendNet(predictor_export_meta.global_init_net)

    # Add the model_id in the predict_net to the global_init_net
    utils.AddModelIdArg(predictor_export_meta, net.Proto())
    return net.Proto()
