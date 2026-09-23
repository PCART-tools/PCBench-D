def conv_picker(func, conv1dOpt, conv2dOpt, conv3dOpt):
    if func == F.conv1d:
        return conv1dOpt
    if func == F.conv2d:
        return conv2dOpt
    else:
        assert func == F.conv3d
        return conv3dOpt
