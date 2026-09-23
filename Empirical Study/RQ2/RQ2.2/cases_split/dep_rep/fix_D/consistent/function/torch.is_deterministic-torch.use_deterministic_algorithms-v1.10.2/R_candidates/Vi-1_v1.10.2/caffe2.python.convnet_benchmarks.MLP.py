def MLP(order, cudnn_ws):
    model = model_helper.ModelHelper(name="MLP")
    d = 256
    depth = 20
    width = 3
    for i in range(depth):
        for j in range(width):
            current = "fc_{}_{}".format(i, j) if i > 0 else "data"
            next_ = "fc_{}_{}".format(i + 1, j)
            brew.fc(
                model,
                current,
                next_,
                dim_in=d,
                dim_out=d,
                weight_init=('XavierFill', {}),
                bias_init=('XavierFill', {}),
            )
    brew.sum(
        model, ["fc_{}_{}".format(depth, j) for j in range(width)], ["sum"]
    )
    brew.fc(
        model,
        "sum",
        "last",
        dim_in=d,
        dim_out=1000,
        weight_init=('XavierFill', {}),
        bias_init=('XavierFill', {}),
    )
    xent = model.net.LabelCrossEntropy(["last", "label"], "xent")
    model.net.AveragedLoss(xent, "loss")
    return model, d
