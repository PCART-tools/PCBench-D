def _InceptionModule(
    model, input_blob, input_depth, output_name, conv1_depth, conv3_depths,
    conv5_depths, pool_depth
):
    # path 1: 1x1 conv
    conv1 = model.Conv(
        input_blob, output_name + ":conv1", input_depth, conv1_depth, 1,
        ('XavierFill', {}), ('ConstantFill', {})
    )
    conv1 = model.Relu(conv1, conv1)
    # path 2: 1x1 conv + 3x3 conv
    conv3_reduce = model.Conv(
        input_blob, output_name +
        ":conv3_reduce", input_depth, conv3_depths[0],
        1, ('XavierFill', {}), ('ConstantFill', {})
    )
    conv3_reduce = model.Relu(conv3_reduce, conv3_reduce)
    conv3 = model.Conv(
        conv3_reduce,
        output_name + ":conv3",
        conv3_depths[0],
        conv3_depths[1],
        3,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=1
    )
    conv3 = model.Relu(conv3, conv3)
    # path 3: 1x1 conv + 5x5 conv
    conv5_reduce = model.Conv(
        input_blob, output_name +
        ":conv5_reduce", input_depth, conv5_depths[0],
        1, ('XavierFill', {}), ('ConstantFill', {})
    )
    conv5_reduce = model.Relu(conv5_reduce, conv5_reduce)
    conv5 = model.Conv(
        conv5_reduce,
        output_name + ":conv5",
        conv5_depths[0],
        conv5_depths[1],
        5,
        ('XavierFill', {}),
        ('ConstantFill', {}),
        pad=2
    )
    conv5 = model.Relu(conv5, conv5)
    # path 4: pool + 1x1 conv
    pool = model.MaxPool(
        input_blob,
        output_name + ":pool",
        kernel=3,
        stride=1,
        pad=1
    )
    pool_proj = model.Conv(
        pool, output_name + ":pool_proj", input_depth, pool_depth, 1,
        ('XavierFill', {}), ('ConstantFill', {})
    )
    pool_proj = model.Relu(pool_proj, pool_proj)
    output = model.Concat([conv1, conv3, conv5, pool_proj], output_name)
    return output
