def alexnet():
    model = ModelHelper(name="r", arg_scope={"order": "NCHW", "is_test": True})
    conv1 = brew.conv(
        model,
        "data",
        "conv1",
        3,
        64,
        11, ('XavierFill', {}), ('ConstantFill', {}),
        stride=4,
        pad=2
    )
    relu1 = brew.relu(model, conv1, "conv1")
    pool1 = brew.max_pool(model, relu1, "pool1", kernel=3, stride=2, pad=0,
                          legacy_pad=3)
    lrn1 = brew.lrn(
        model, pool1, "pool1_lrn", size=5, alpha=1.0e-4, beta=0.75, bias=1.0)
    conv2 = brew.conv(
        model,
        lrn1,
        "conv2",
        64,
        192,
        5,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=2
    )
    relu2 = brew.relu(model, conv2, "conv2")
    pool2 = brew.max_pool(model, relu2, "pool2", kernel=3, stride=2)
    lrn2 = brew.lrn(
        model, pool2, "pool2_lrn", size=5, alpha=1.0e-4, beta=0.75, bias=1.0)
    conv3 = brew.conv(
        model,
        lrn2,
        "conv3",
        192,
        384,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu3 = brew.relu(model, conv3, "conv3")
    conv4 = brew.conv(
        model,
        relu3,
        "conv4",
        384,
        256,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu4 = brew.relu(model, conv4, "conv4")
    conv5 = brew.conv(
        model,
        relu4,
        "conv5",
        256,
        256,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu5 = brew.relu(model, conv5, "conv5")
    pool5 = brew.max_pool(model, relu5, "pool5", kernel=3, stride=2)
    fc6 = brew.fc(
        model,
        pool5, "fc6", 256 * 6 * 6, 4096, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    relu6 = brew.relu(model, fc6, "fc6")
    fc7 = brew.fc(
        model, relu6, "fc7", 4096, 4096, ('XavierFill', {}), ('ConstantFill', {})
    )
    relu7 = brew.relu(model, fc7, "fc7")
    drop7 = brew.dropout(model, relu7, "fc7_dropout", is_test=1, ratio=0.5)
    fc8 = brew.fc(
        model, drop7, "fc8", 4096, 1000, ('XavierFill', {}), ('ConstantFill', {})
    )
    relu8 = brew.relu(model, fc8, "fc8")
    brew.dropout(model, relu8, "fc8_dropout", is_test=1, ratio=0.5)
    return model, [(1, 3, 224, 224)]
