def OverFeat(order):
    model = cnn.CNNModelHelper(order, name="overfeat",
                               use_cudnn=True, cudnn_exhaustive_search=True)
    conv1 = model.Conv(
        "data",
        "conv1",
        3,
        96,
        11,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        stride=4
    )
    relu1 = model.Relu(conv1, "conv1")
    pool1 = model.MaxPool(relu1, "pool1", kernel=2, stride=2)
    conv2 = model.Conv(
        pool1, "conv2", 96, 256, 5, ('XavierFill', {}), ('ConstantFill', {})
    )
    relu2 = model.Relu(conv2, "conv2")
    pool2 = model.MaxPool(relu2, "pool2", kernel=2, stride=2)
    conv3 = model.Conv(
        pool2,
        "conv3",
        256,
        512,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu3 = model.Relu(conv3, "conv3")
    conv4 = model.Conv(
        relu3,
        "conv4",
        512,
        1024,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu4 = model.Relu(conv4, "conv4")
    conv5 = model.Conv(
        relu4,
        "conv5",
        1024,
        1024,
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    relu5 = model.Relu(conv5, "conv5")
    pool5 = model.MaxPool(relu5, "pool5", kernel=2, stride=2)
    fc6 = model.FC(
        pool5, "fc6", 1024 * 6 * 6, 3072, ('XavierFill', {}),
        ('ConstantFill', {})
    )
    relu6 = model.Relu(fc6, "fc6")
    fc7 = model.FC(
        relu6, "fc7", 3072, 4096, ('XavierFill', {}), ('ConstantFill', {})
    )
    relu7 = model.Relu(fc7, "fc7")
    fc8 = model.FC(
        relu7, "fc8", 4096, 1000, ('XavierFill', {}), ('ConstantFill', {})
    )
    pred = model.Softmax(fc8, "pred")
    xent = model.LabelCrossEntropy([pred, "label"], "xent")
    model.AveragedLoss(xent, "loss")
    return model, 231
