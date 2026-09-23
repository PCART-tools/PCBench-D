def VGGA(order, cudnn_ws):
    my_arg_scope = {
        'order': order,
        'use_cudnn': True,
        'cudnn_exhaustive_search': True,
    }
    if cudnn_ws:
        my_arg_scope['ws_nbytes_limit'] = cudnn_ws
    model = model_helper.ModelHelper(
        name="vgga",
        arg_scope=my_arg_scope,
    )
    conv1 = brew.conv(
        model,
        "data",
        "conv1",
        3,
        64,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu1 = brew.relu(model, conv1, "conv1")
    pool1 = brew.max_pool(model, relu1, "pool1", kernel=2, stride=2)
    conv2 = brew.conv(
        model,
        pool1,
        "conv2",
        64,
        128,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu2 = brew.relu(model, conv2, "conv2")
    pool2 = brew.max_pool(model, relu2, "pool2", kernel=2, stride=2)
    conv3 = brew.conv(
        model,
        pool2,
        "conv3",
        128,
        256,
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
        256,
        256,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu4 = brew.relu(model, conv4, "conv4")
    pool4 = brew.max_pool(model, relu4, "pool4", kernel=2, stride=2)
    conv5 = brew.conv(
        model,
        pool4,
        "conv5",
        256,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu5 = brew.relu(model, conv5, "conv5")
    conv6 = brew.conv(
        model,
        relu5,
        "conv6",
        512,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu6 = brew.relu(model, conv6, "conv6")
    pool6 = brew.max_pool(model, relu6, "pool6", kernel=2, stride=2)
    conv7 = brew.conv(
        model,
        pool6,
        "conv7",
        512,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu7 = brew.relu(model, conv7, "conv7")
    conv8 = brew.conv(
        model,
        relu7,
        "conv8",
        512,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu8 = brew.relu(model, conv8, "conv8")
    pool8 = brew.max_pool(model, relu8, "pool8", kernel=2, stride=2)

    fcix = brew.fc(
        model, pool8, "fcix", 512 * 7 * 7, 4096, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    reluix = brew.relu(model, fcix, "fcix")
    fcx = brew.fc(
        model, reluix, "fcx", 4096, 4096, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    relux = brew.relu(model, fcx, "fcx")
    fcxi = brew.fc(
        model, relux, "fcxi", 4096, 1000, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    pred = brew.softmax(model, fcxi, "pred")
    xent = model.net.LabelCrossEntropy([pred, "label"], "xent")
    model.net.AveragedLoss(xent, "loss")
    return model, 231
