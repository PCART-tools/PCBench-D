def simple_cnn():
    model = ModelHelper(name="r", arg_scope={"order": "NCHW", "is_test": True})
    brew.conv(
        model, "data", 'conv1', 3, 16, kernel=3, stride=1
    )
    brew.spatial_bn(
        model, 'conv1', 'conv1_spatbn', 16, epsilon=1e-3
    )
    brew.relu(model, 'conv1_spatbn', 'relu1')
    return model, [(1, 3, 32, 32)]
