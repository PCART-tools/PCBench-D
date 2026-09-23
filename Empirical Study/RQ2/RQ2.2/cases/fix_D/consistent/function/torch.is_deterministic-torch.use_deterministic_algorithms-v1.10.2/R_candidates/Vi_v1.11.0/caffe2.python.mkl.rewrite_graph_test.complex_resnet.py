def complex_resnet():
    model = ModelHelper(name="r", arg_scope={"order": "NCHW", "is_test": True})
    resnet.create_resnet50(
        model, "data", num_input_channels=1, num_labels=5, is_test=True,
        no_loss=True)
    return model, [(1, 1, 224, 224)]
