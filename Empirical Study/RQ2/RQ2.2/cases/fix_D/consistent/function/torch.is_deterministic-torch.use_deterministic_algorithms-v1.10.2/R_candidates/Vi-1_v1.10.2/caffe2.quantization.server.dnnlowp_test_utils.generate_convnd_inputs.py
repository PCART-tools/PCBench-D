def generate_convnd_inputs(
    strides,
    pads,
    kernels,
    dilations,
    sizes,
    group,
    input_channels_per_group,
    output_channels_per_group,
    batch_size,
    order,
    groupwise_quantization=False,
    preserve_activation_sparsity=False,
    preserve_weight_sparsity=False,
):
    dim = len(sizes)
    assume(all(len(a) == dim for a in [strides, pads, kernels, dilations]))
    assume(all(sizes[d] >= dilations[d] * (kernels[d] - 1) + 1 for d in range(dim)))
    input_channels = input_channels_per_group * group
    output_channels = output_channels_per_group * group
    depthwise_convolution = (
        input_channels_per_group == 1 and output_channels_per_group == 1
    )

    assert input_channels > 1
    assert output_channels > 1

    # X and W have scale 1, so exactly represented after quantization
    X_min = 0 if preserve_activation_sparsity else -77
    X_max = X_min + 255
    X_range = X_max - X_min
    if depthwise_convolution and groupwise_quantization:
        # For depthwise convolution, it's not enough to set input channel 0
        # to all X_min to avoid overflow from vpmaddubsw
        X_range /= 2
    X = np.round(
        np.random.rand(*((batch_size,) + tuple(sizes) + (input_channels,))) * X_range
        + X_min
    )
    X = X.astype(np.float32)
    if (
        batch_size != 0
        and depthwise_convolution
        and groupwise_quantization
        and not preserve_activation_sparsity
    ):
        # Put X_max in a position not to be paired with any padded value.
        # Put X_min to all positions that can be paired with the X_max value.
        #
        # This is an example of a pattern for 3x3x3
        #  .   .   .   .   .
        #  .   .   .   .   .
        #  .   .   .   .   .
        #  .   .   .   .   .
        #  .   .   .   .  min
        #
        #  .   .   .   .   .
        #  .   .   .   .  min
        #  .  min max min  .
        # min  .   .   .   .
        #  .   .   .   .   .
        #
        # min  .   .   .   .
        #  .   .   .   .   .
        #  .   .   .   .   .
        #  .   .   .   .   .
        #  .   .   .   .   .

        # Make sure we have enough dimension
        assert X.shape[1] >= 3
        assert all(X.shape[d + 1] >= kernels[d] + 2 for d in range(1, dim))

        # Take subtensor we want to manipulate
        X_sub = X[(0,) * (X.ndim - dim - 1) + (slice(None),) * dim + (0,)]

        # Put X_max in the middle of the subtensor
        X_sub[(1,) + tuple(kernels[d] // 2 + 1 for d in range(1, dim))] = X_max

        # Put X_min to the positions that can be paired with X_max across
        # the slowest moving dimension
        X_sub[[[0, 2]] + [[kernels[d] + 1, 0] for d in range(1, dim)]] = X_min

        # Put X_min to other positions that can be paired with X_max
        for d1 in range(1, dim):
            X_sub[
                [[1]]
                + [[kernels[d2] // 2 + 1] for d2 in range(1, d1)]
                + [[kernels[d1] // 2, kernels[d1] // 2 + 2]]
                + [[kernels[d2] + 1, 0] for d2 in range(d1 + 1, dim)]
            ] = X_min
    else:
        # input channel 0 is all X_min to avoid overflow from vpmaddubsw when
        # multiplied with W_min and W_max
        X[..., 0] = X_min
        if batch_size != 0:
            X[(0,) * (X.ndim - 1) + (1,)] = X_max

    if preserve_weight_sparsity:
        W_min = -128
        W_max = 100
    else:
        W_min = -100
        W_max = W_min + 255
    W = np.round(
        np.random.rand(
            *((output_channels,) + tuple(kernels) + (input_channels_per_group,))
        )
        * (W_max - W_min)
        + W_min
    )
    W = W.astype(np.float32)
    if groupwise_quantization:
        for g in range(group):
            W[(g * output_channels_per_group,) + (0,) * (W.ndim - 1)] = W_min
            if depthwise_convolution:
                W[(g * output_channels_per_group, 1) + (0,) * (W.ndim - 2)] = W_max
            else:
                assert output_channels_per_group > 1
                W[(g * output_channels_per_group + 1,) + (0,) * (W.ndim - 1)] = W_max

            # Make sure each group has different ranges to really see the effect
            # of group-wise quantization.
            if not preserve_weight_sparsity:
                W[
                    g * output_channels_per_group : (g + 1) * output_channels_per_group,
                ] += g
    else:
        W[(0,) + (0,) * (W.ndim - 1)] = W_min
        W[(1,) + (0,) * (W.ndim - 1)] = W_max

    different_range_per_group = groupwise_quantization and not preserve_weight_sparsity
    for g in range(group):
        avoid_vpmaddubsw_overflow(
            strides,
            pads,
            kernels,
            dilations,
            sizes,
            input_channels_per_group,
            output_channels_per_group,
            batch_size,
            X[..., g * input_channels_per_group : (g + 1) * input_channels_per_group],
            X_min,
            X_max,
            W[g * output_channels_per_group : (g + 1) * output_channels_per_group,],
            W_min + (g if different_range_per_group else 0),
            W_max + (g if different_range_per_group else 0),
        )

    if order == "NCHW":
        X = utils.NHWC2NCHW(X)
        W = utils.NHWC2NCHW(W)

    b = np.random.randn(output_channels).astype(np.float32)

    return X, W, b
