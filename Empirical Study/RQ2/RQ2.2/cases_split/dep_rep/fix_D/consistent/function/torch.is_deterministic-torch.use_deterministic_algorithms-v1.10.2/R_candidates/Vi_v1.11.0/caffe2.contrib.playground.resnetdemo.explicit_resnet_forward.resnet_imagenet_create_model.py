def resnet_imagenet_create_model(model, data, labels, split, opts, dataset):
    model_helper = ResNetModelHelper(model, split, opts)
    opts_depth = opts['model_param']['num_layer']
    engine = opts['model_param']['engine']
    log.info(' | ResNet-{} Imagenet'.format(opts_depth))
    assert opts_depth in BLOCK_CONFIG.keys(), \
        'Block config is not defined for specified model depth. Please check.'
    (n1, n2, n3, n4) = BLOCK_CONFIG[opts_depth]

    num_features = 2048
    residual_block = model_helper.bottleneck_block
    if opts_depth in [18, 34]:
        num_features = 512
        residual_block = model_helper.basic_block

    num_classes = 1000
    conv_blob = model.Conv(
        data, 'conv1', 3, 64, 7, stride=2, pad=3, weight_init=('MSRAFill', {}),
        bias_init=('ConstantFill', {'value': 0.}), no_bias=0, engine=engine
    )
    test_mode = False
    if split in ['test', 'val']:
        test_mode = True
    bn_blob = model.SpatialBN(
        conv_blob, 'res_conv1_bn', 64,
        # does not appear to affect test_loss performance
        # epsilon=1e-3,
        epsilon=opts['model_param']['bn_epsilon'],
        # momentum=0.1,
        momentum=opts['model_param']['bn_momentum'],
        is_test=test_mode,
    )
    relu_blob = model.Relu(bn_blob, bn_blob)
    max_pool = model.MaxPool(relu_blob, 'pool1', kernel=3, stride=2, pad=1)

    # TODO: This can be further optimized by passing dim_in, dim_out = features,
    # dim_out = features * 4
    if opts_depth in [50, 101, 152, 200, 264, 284]:
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, max_pool, 64, 256, stride=1, num_blocks=n1,
            prefix='res2', dim_inner=64
        )
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, blob_in, dim_in, 512, stride=2, num_blocks=n2,
            prefix='res3', dim_inner=128
        )
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, blob_in, dim_in, 1024, stride=2, num_blocks=n3,
            prefix='res4', dim_inner=256
        )
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, blob_in, dim_in, 2048, stride=2, num_blocks=n4,
            prefix='res5', dim_inner=512
        )
    elif opts_depth in [18, 34]:
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, max_pool, 64, 64, stride=1, num_blocks=n1,
            prefix='res2',
        )
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, blob_in, dim_in, 128, stride=2, num_blocks=n2,
            prefix='res3',
        )
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, blob_in, dim_in, 256, stride=2, num_blocks=n3,
            prefix='res4',
        )
        blob_in, dim_in = model_helper.residual_layer(
            residual_block, blob_in, dim_in, 512, stride=2, num_blocks=n4,
            prefix='res5',
        )

    pool_blob = model.AveragePool(blob_in, 'pool5', kernel=7, stride=1)

    loss_scale = 1. / opts['distributed']['num_xpus'] / \
        opts['distributed']['num_shards']

    loss = None

    fc_blob = model.FC(
        pool_blob, 'pred', num_features, num_classes,
        # does not appear to affect test_loss performance
        # weight_init=('GaussianFill', {'std': opts.fc_init_std}),
        # bias_init=('ConstantFill', {'value': 0.})
        weight_init=None,
        bias_init=None)
    softmax, loss = model.SoftmaxWithLoss(
        [fc_blob, labels],
        ['softmax', 'loss'],
        scale=loss_scale)
    model.Accuracy(['softmax', labels], 'accuracy')
    return model, softmax, loss
