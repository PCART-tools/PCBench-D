def Inception(order, cudnn_ws):
    my_arg_scope = {
        'order': order,
        'use_cudnn': True,
        'cudnn_exhaustive_search': True,
    }
    if cudnn_ws:
        my_arg_scope['ws_nbytes_limit'] = cudnn_ws
    model = model_helper.ModelHelper(
        name="inception",
        arg_scope=my_arg_scope,
    )
    conv1 = brew.conv(
        model,
        "data",
        "conv1",
        3,
        64,
        7,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        stride=2,
        pad=3,
    )
    relu1 = brew.relu(model, conv1, "conv1")
    pool1 = brew.max_pool(model, relu1, "pool1", kernel=3, stride=2, pad=1)
    conv2a = brew.conv(
        model, pool1, "conv2a", 64, 64, 1, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    conv2a = brew.relu(model, conv2a, conv2a)
    conv2 = brew.conv(
        model,
        conv2a,
        "conv2",
        64,
        192,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    relu2 = brew.relu(model, conv2, "conv2")
    pool2 = brew.max_pool(model, relu2, "pool2", kernel=3, stride=2, pad=1)
    # Inception modules
    inc3 = _InceptionModule(
        model, pool2, 192, "inc3", 64, [96, 128], [16, 32], 32
    )
    inc4 = _InceptionModule(
        model, inc3, 256, "inc4", 128, [128, 192], [32, 96], 64
    )
    pool5 = brew.max_pool(model, inc4, "pool5", kernel=3, stride=2, pad=1)
    inc5 = _InceptionModule(
        model, pool5, 480, "inc5", 192, [96, 208], [16, 48], 64
    )
    inc6 = _InceptionModule(
        model, inc5, 512, "inc6", 160, [112, 224], [24, 64], 64
    )
    inc7 = _InceptionModule(
        model, inc6, 512, "inc7", 128, [128, 256], [24, 64], 64
    )
    inc8 = _InceptionModule(
        model, inc7, 512, "inc8", 112, [144, 288], [32, 64], 64
    )
    inc9 = _InceptionModule(
        model, inc8, 528, "inc9", 256, [160, 320], [32, 128], 128
    )
    pool9 = brew.max_pool(model, inc9, "pool9", kernel=3, stride=2, pad=1)
    inc10 = _InceptionModule(
        model, pool9, 832, "inc10", 256, [160, 320], [32, 128], 128
    )
    inc11 = _InceptionModule(
        model, inc10, 832, "inc11", 384, [192, 384], [48, 128], 128
    )
    pool11 = brew.average_pool(model, inc11, "pool11", kernel=7, stride=1)
    fc = brew.fc(
        model, pool11, "fc", 1024, 1000, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    # It seems that Soumith's benchmark does not have softmax on top
    # for Inception. We will add it anyway so we can have a proper
    # backward pass.
    pred = brew.softmax(model, fc, "pred")
    xent = model.net.LabelCrossEntropy([pred, "label"], "xent")
    model.net.AveragedLoss(xent, "loss")
    return model, 224
