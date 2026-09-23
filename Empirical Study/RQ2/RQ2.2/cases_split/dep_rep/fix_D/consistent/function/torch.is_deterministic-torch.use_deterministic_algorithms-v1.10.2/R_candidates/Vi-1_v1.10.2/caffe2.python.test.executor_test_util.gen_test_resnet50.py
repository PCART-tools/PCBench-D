def gen_test_resnet50(_order, _cudnn_ws):
    model = cnn.CNNModelHelper(
        order="NCHW",
        name="resnet_50_test",
        cudnn_exhaustive_search=True,
    )
    data = model.net.AddExternalInput("data")
    label = model.net.AddExternalInput("label")
    (_softmax, loss) = resnet.create_resnet50(
        model,
        data,
        num_input_channels=3,
        num_labels=1000,
        label=label,
        is_test=False,
    )
    return model, 227
