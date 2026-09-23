def get_meta_net_def(predictor_export_meta, ws=None, db_type=None):
    """
    """

    ws = ws or workspace.C.Workspace.current
    meta_net_def = metanet_pb2.MetaNetDef()

    # Predict net is the core network that we use.
    utils.AddNet(meta_net_def, predictor_export_meta.predict_init_name(),
                 utils.create_predict_init_net(ws, predictor_export_meta))
    utils.AddNet(meta_net_def, predictor_export_meta.global_init_name(),
                 _global_init_net(predictor_export_meta, db_type))
    utils.AddNet(meta_net_def, predictor_export_meta.predict_net_name(),
                 utils.create_predict_net(predictor_export_meta))
    utils.AddBlobs(meta_net_def, predictor_export_meta.parameters_name(),
                   predictor_export_meta.parameters)
    utils.AddBlobs(meta_net_def, predictor_export_meta.inputs_name(),
                   predictor_export_meta.inputs)
    utils.AddBlobs(meta_net_def, predictor_export_meta.outputs_name(),
                   predictor_export_meta.outputs)
    return meta_net_def
