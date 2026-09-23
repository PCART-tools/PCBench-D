def create_resnext(
    model,
    data,
    num_input_channels,
    num_labels,
    num_layers,
    num_groups,
    num_width_per_group,
    label=None,
    is_test=False,
    no_loss=False,
    no_bias=1,
    conv1_kernel=7,
    conv1_stride=2,
    final_avg_kernel=7,
    log=None,
    bn_epsilon=1e-5,
    bn_momentum=0.9,
):
    if num_layers not in RESNEXT_BLOCK_CONFIG:
        log.error("{}-layer is invalid for resnext config".format(num_layers))

    num_blocks = RESNEXT_BLOCK_CONFIG[num_layers]
    strides = RESNEXT_STRIDES
    num_filters = [64, 256, 512, 1024, 2048]

    if num_layers in [18, 34]:
        num_filters = [64, 64, 128, 256, 512]

    # the number of features before the last FC layer
    num_features = num_filters[-1]

    # conv1 + maxpool
    conv_blob = brew.conv(
        model,
        data,
        'conv1',
        num_input_channels,
        num_filters[0],
        weight_init=("MSRAFill", {}),
        kernel=conv1_kernel,
        stride=conv1_stride,
        pad=3,
        no_bias=no_bias
    )

    bn_blob = brew.spatial_bn(
        model,
        conv_blob,
        'conv1_spatbn_relu',
        num_filters[0],
        epsilon=bn_epsilon,
        momentum=bn_momentum,
        is_test=is_test
    )
    relu_blob = brew.relu(model, bn_blob, bn_blob)
    max_pool = brew.max_pool(model, relu_blob, 'pool1', kernel=3, stride=2, pad=1)

    # Residual blocks...
    builder = ResNetBuilder(model, max_pool, no_bias=no_bias,
                            is_test=is_test, bn_epsilon=1e-5, bn_momentum=0.9)

    inner_dim = num_groups * num_width_per_group

    # 4 different kinds of residual blocks
    for residual_idx in range(4):
        residual_num = num_blocks[residual_idx]
        residual_stride = strides[residual_idx]
        dim_in = num_filters[residual_idx]

        for blk_idx in range(residual_num):
            dim_in = builder.add_bottleneck(
                dim_in,
                inner_dim,
                num_filters[residual_idx + 1],  # dim out
                stride=residual_stride if blk_idx == 0 else 1,
                group=num_groups,
            )

        inner_dim *= 2

    # Final layers
    final_avg = brew.average_pool(
        model,
        builder.prev_blob,
        'final_avg',
        kernel=final_avg_kernel,
        stride=1,
        global_pooling=True,
    )

    # Final dimension of the "image" is reduced to 7x7
    last_out = brew.fc(
        model, final_avg, 'last_out_L{}'.format(num_labels), num_features, num_labels
    )

    if no_loss:
        return last_out

    # If we create model for training, use softmax-with-loss
    if (label is not None):
        (softmax, loss) = model.SoftmaxWithLoss(
            [last_out, label],
            ["softmax", "loss"],
        )

        return (softmax, loss)
    else:
        # For inference, we just return softmax
        return brew.softmax(model, last_out, "softmax")
