def create_shufflenet(
    model,
    data,
    num_input_channels,
    num_labels,
    label=None,
    is_test=False,
    no_loss=False,
):
    builder = ShuffleNetV2Builder(model, data, num_input_channels,
                                  num_labels,
                                  is_test=is_test)
    builder.create()

    if no_loss:
        return builder.last_out

    if (label is not None):
        (softmax, loss) = model.SoftmaxWithLoss(
            [builder.last_out, label],
            ["softmax", "loss"],
        )
        return (softmax, loss)
