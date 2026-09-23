def _InceptionModule(
    model, input_blob, input_depth, output_name, conv1_depth, conv3_depths,
    conv5_depths, pool_depth
):
    # path 1: 1x1 conv
    conv1 = brew.conv(
        model, input_blob, output_name + ":conv1", input_depth, conv1_depth, 1,
        ('XavierFill', {}), ('ConstantFill', {})
    )
    conv1 = brew.relu(model, conv1, conv1)
    # path 2: 1x1 conv + 3x3 conv
    conv3_reduce = brew.conv(
        model, input_blob, output_name + ":conv3_reduce", input_depth,
        conv3_depths[0], 1, ('XavierFill', {}), ('ConstantFill', {})
    )
    conv3_reduce = brew.relu(model, conv3_reduce, conv3_reduce)
    conv3 = brew.conv(
        model,
        conv3_reduce,
        output_name + ":conv3",
        conv3_depths[0],
        conv3_depths[1],
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1,
    )
    conv3 = brew.relu(model, conv3, conv3)
    # path 3: 1x1 conv + 5x5 conv
    conv5_reduce = brew.conv(
        model, input_blob, output_name + ":conv5_reduce", input_depth,
        conv5_depths[0], 1, ('XavierFill', {}), ('ConstantFill', {})
    )
    conv5_reduce = brew.relu(model, conv5_reduce, conv5_reduce)
    conv5 = brew.conv(
        model,
        conv5_reduce,
        output_name + ":conv5",
        conv5_depths[0],
        conv5_depths[1],
        5,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=2,
    )
    conv5 = brew.relu(model, conv5, conv5)
    # path 4: pool + 1x1 conv
    pool = brew.max_pool(
        model,
        input_blob,
        output_name + ":pool",
        kernel=3,
        stride=1,
        pad=1,
    )
    pool_proj = brew.conv(
        model, pool, output_name + ":pool_proj", input_depth, pool_depth, 1,
        ('XavierFill', {}), ('ConstantFill', {})
    )
    pool_proj = brew.relu(model, pool_proj, pool_proj)
    output = brew.concat(model, [conv1, conv3, conv5, pool_proj], output_name)
    return output
