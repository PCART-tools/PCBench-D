def OverFeat(order, cudnn_ws):
    my_arg_scope = {
        'order': order,
        'use_cudnn': True,
        'cudnn_exhaustive_search': True,
    }
    if cudnn_ws:
        my_arg_scope['ws_nbytes_limit'] = cudnn_ws
    model = model_helper.ModelHelper(
        name="overfeat",
        arg_scope=my_arg_scope,
    )
    conv1 = brew.conv(
        model,
        "data",
        "conv1",
        3,
        96,
        11,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        stride=4,
    )
    relu1 = brew.relu(model, conv1, "conv1")
    pool1 = brew.max_pool(model, relu1, "pool1", kernel=2, stride=2)
    conv2 = brew.conv(
        model, pool1, "conv2", 96, 256, 5, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    relu2 = brew.relu(model, conv2, "conv2")
    pool2 = brew.max_pool(model, relu2, "pool2", kernel=2, stride=2)
    conv3 = brew.conv(
        model,
        pool2,
        "conv3",
        256,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu3 = brew.relu(model, conv3, "conv3")
    conv4 = brew.conv(
        model,
        relu3,
        "conv4",
        512,
        1024,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu4 = brew.relu(model, conv4, "conv4")
    conv5 = brew.conv(
        model,
        relu4,
        "conv5",
        1024,
        1024,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu5 = brew.relu(model, conv5, "conv5")
    pool5 = brew.max_pool(model, relu5, "pool5", kernel=2, stride=2)
    fc6 = brew.fc(
        model, pool5, "fc6", 1024 * 6 * 6, 3072, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    relu6 = brew.relu(model, fc6, "fc6")
    fc7 = brew.fc(
        model, relu6, "fc7", 3072, 4096, ('XavierFill', {}), ('ConstantFill', {})
    )
    relu7 = brew.relu(model, fc7, "fc7")
    fc8 = brew.fc(
        model, relu7, "fc8", 4096, 1000, ('XavierFill', {}), ('ConstantFill', {})
    )
    pred = brew.softmax(model, fc8, "pred")
    xent = model.net.LabelCrossEntropy([pred, "label"], "xent")
    model.net.AveragedLoss(xent, "loss")
    return model, 231
