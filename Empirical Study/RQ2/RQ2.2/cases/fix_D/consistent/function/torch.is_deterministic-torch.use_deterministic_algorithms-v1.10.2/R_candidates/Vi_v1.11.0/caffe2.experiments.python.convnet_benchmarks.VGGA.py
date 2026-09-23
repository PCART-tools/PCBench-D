def VGGA(order):
    model = cnn.CNNModelHelper(order, name='vgg-a',
                               use_cudnn=True, cudnn_exhaustive_search=True)
    conv1 = model.Conv(
        "data",
        "conv1",
        3,
        64,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu1 = model.Relu(conv1, "conv1")
    pool1 = model.MaxPool(relu1, "pool1", kernel=2, stride=2)
    conv2 = model.Conv(
        pool1,
        "conv2",
        64,
        128,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu2 = model.Relu(conv2, "conv2")
    pool2 = model.MaxPool(relu2, "pool2", kernel=2, stride=2)
    conv3 = model.Conv(
        pool2,
        "conv3",
        128,
        256,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu3 = model.Relu(conv3, "conv3")
    conv4 = model.Conv(
        relu3,
        "conv4",
        256,
        256,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu4 = model.Relu(conv4, "conv4")
    pool4 = model.MaxPool(relu4, "pool4", kernel=2, stride=2)
    conv5 = model.Conv(
        pool4,
        "conv5",
        256,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu5 = model.Relu(conv5, "conv5")
    conv6 = model.Conv(
        relu5,
        "conv6",
        512,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu6 = model.Relu(conv6, "conv6")
    pool6 = model.MaxPool(relu6, "pool6", kernel=2, stride=2)
    conv7 = model.Conv(
        pool6,
        "conv7",
        512,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu7 = model.Relu(conv7, "conv7")
    conv8 = model.Conv(
        relu7,
        "conv8",
        512,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu8 = model.Relu(conv8, "conv8")
    pool8 = model.MaxPool(relu8, "pool8", kernel=2, stride=2)

    fcix = model.FC(
        pool8, "fcix", 512 * 7 * 7, 4096, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    reluix = model.Relu(fcix, "fcix")
    fcx = model.FC(
        reluix, "fcx", 4096, 4096, ('XavierFill', {}), ('ConstantFill', {})
    )
    relux = model.Relu(fcx, "fcx")
    fcxi = model.FC(
        relux, "fcxi", 4096, 1000, ('XavierFill', {}), ('ConstantFill', {})
    )
    pred = model.Softmax(fcxi, "pred")
    xent = model.LabelCrossEntropy([pred, "label"], "xent")
    model.AveragedLoss(xent, "loss")
    return model, 231
