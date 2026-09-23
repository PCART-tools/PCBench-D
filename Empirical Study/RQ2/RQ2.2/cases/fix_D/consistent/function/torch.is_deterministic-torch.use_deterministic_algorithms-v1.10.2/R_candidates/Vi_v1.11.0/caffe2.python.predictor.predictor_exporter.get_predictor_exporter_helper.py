def get_predictor_exporter_helper(submodelNetName):
    """ constracting stub for the PredictorExportMeta
        Only used to construct names to subfields,
        such as calling to predict_net_name
        Args:
            submodelNetName - name of the model
    """
    stub_net = core.Net(submodelNetName)
    pred_meta = PredictorExportMeta(predict_net=stub_net,
                                    parameters=[],
                                    inputs=[],
                                    outputs=[],
                                    shapes=None,
                                    name=submodelNetName,
                                    extra_init_net=None)
    return pred_meta
