def MLP(order):
    model = cnn.CNNModelHelper()
    d = 256
    depth = 20
    width = 3
    for i in range(depth):
        for j in range(width):
            current = "fc_{}_{}".format(i, j) if i > 0 else "data"
            next_ = "fc_{}_{}".format(i + 1, j)
            model.FC(
                current, next_,
                dim_in=d, dim_out=d,
                weight_init=model.XavierInit,
                bias_init=model.XavierInit)
            model.Sum(["fc_{}_{}".format(depth, j)
                       for j in range(width)], ["sum"])
            model.FC("sum", "last",
                     dim_in=d, dim_out=1000,
                     weight_init=model.XavierInit,
                     bias_init=model.XavierInit)
            xent = model.LabelCrossEntropy(["last", "label"], "xent")
            model.AveragedLoss(xent, "loss")
            return model, d
