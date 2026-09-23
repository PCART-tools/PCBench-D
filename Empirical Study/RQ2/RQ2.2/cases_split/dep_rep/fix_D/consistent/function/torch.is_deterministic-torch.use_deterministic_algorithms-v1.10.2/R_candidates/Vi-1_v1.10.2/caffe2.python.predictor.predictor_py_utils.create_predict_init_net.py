def create_predict_init_net(ws, predictor_export_meta):
    """
    Return an initialization net that zero-fill all the input and
    output blobs, using the shapes from the provided workspace. This is
    necessary as there is no shape inference functionality in Caffe2.
    """
    net = core.Net("predict-init")

    def zero_fill(blob):
        shape = predictor_export_meta.shapes.get(blob)
        if shape is None:
            if blob not in ws.blobs:
                raise Exception(
                    "{} not in workspace but needed for shape: {}".format(
                        blob, ws.blobs
                    )
                )

            shape = ws.blobs[blob].fetch().shape

        # Explicitly null-out the scope so users (e.g. PredictorGPU)
        # can control (at a Net-global level) the DeviceOption of
        # these filling operators.
        with scope.EmptyDeviceScope():
            net.ConstantFill([], blob, shape=shape, value=0.0)

    external_blobs = predictor_export_meta.inputs + predictor_export_meta.outputs
    for blob in external_blobs:
        zero_fill(blob)

    net.Proto().external_input.extend(external_blobs)
    if predictor_export_meta.extra_init_net:
        net.AppendNet(predictor_export_meta.extra_init_net)

    # Add the model_id in the predict_net to the init_net
    AddModelIdArg(predictor_export_meta, net.Proto())

    return net.Proto()
