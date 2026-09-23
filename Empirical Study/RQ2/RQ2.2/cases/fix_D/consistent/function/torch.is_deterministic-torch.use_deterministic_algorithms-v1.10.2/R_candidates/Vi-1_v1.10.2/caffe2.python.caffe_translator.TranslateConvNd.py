@TranslatorRegistry.Register("Convolution3D")
def TranslateConvNd(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.convolution3d_param
    caffe_op = BaseTranslate(layer, "Conv")
    output = caffe_op.output[0]
    caffe_op.input.append(output + '_w')

    AddArgument(
        caffe_op,
        "kernels",
        [param.kernel_depth, param.kernel_size, param.kernel_size])
    AddArgument(
        caffe_op,
        "strides",
        [param.temporal_stride, param.stride, param.stride])
    temporal_pad = 0
    spatial_pad = 0
    if hasattr(param, 'temporal_pad'):
        temporal_pad = param.temporal_pad
    if hasattr(param, 'pad'):
        spatial_pad = param.pad
    AddArgument(caffe_op, "pads", [temporal_pad, spatial_pad, spatial_pad] * 2)

    # weight
    params = [
        utils.NumpyArrayToCaffe2Tensor(pretrained_blobs[0], output + '_w')]
    # bias
    if len(pretrained_blobs) == 2:
        caffe_op.input.append(output + '_b')
        params.append(
            utils.NumpyArrayToCaffe2Tensor(
                pretrained_blobs[1].flatten(), output + '_b'))
    return caffe_op, params
