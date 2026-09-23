def simple_resnet():
    model = ModelHelper(name="r", arg_scope={"order": "NCHW", "is_test": True})
    resnet.create_resnet_32x32(
        model, "data", num_input_channels=1, num_groups=1, num_labels=5,
        is_test=True)
    return model, [(1, 1, 32, 32)]
