def create_resnet_32x32(
    model, data, num_input_channels, num_groups, num_labels, is_test=False
):
    '''
    Create residual net for smaller images (sec 4.2 of He et. al (2015))
    num_groups = 'n' in the paper
    '''
    # conv1 + maxpool
    brew.conv(
        model, data, 'conv1', num_input_channels, 16, kernel=3, stride=1
    )
    brew.spatial_bn(
        model, 'conv1', 'conv1_spatbn', 16, epsilon=1e-3, is_test=is_test
    )
    brew.relu(model, 'conv1_spatbn', 'relu1')

    # Number of blocks as described in sec 4.2
    filters = [16, 32, 64]

    builder = ResNetBuilder(model, 'relu1', no_bias=0, is_test=is_test)
    prev_filters = 16
    for groupidx in range(0, 3):
        for blockidx in range(0, 2 * num_groups):
            builder.add_simple_block(
                prev_filters if blockidx == 0 else filters[groupidx],
                filters[groupidx],
                down_sampling=(True if blockidx == 0 and
                               groupidx > 0 else False))
        prev_filters = filters[groupidx]

    # Final layers
    brew.average_pool(
        model, builder.prev_blob, 'final_avg', kernel=8, stride=1
    )
    brew.fc(model, 'final_avg', 'last_out', 64, num_labels)
    softmax = brew.softmax(model, 'last_out', 'softmax')
    return softmax
