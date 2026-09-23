@TranslatorRegistry.Register("Convolution")
def TranslateConv(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.convolution_param
    caffe_op = BaseTranslate(layer, "Conv")
    output = caffe_op.output[0]
    caffe_op.input.append(output + '_w')
    _TranslateStridePadKernelHelper(param, caffe_op)
    # weight
    params = [
        utils.NumpyArrayToCaffe2Tensor(pretrained_blobs[0], output + '_w')]
    # bias
    if len(pretrained_blobs) == 2:
        caffe_op.input.append(output + '_b')
        params.append(
            utils.NumpyArrayToCaffe2Tensor(
                pretrained_blobs[1].flatten(), output + '_b'))
    # Group convolution option
    if param.group != 1:
        AddArgument(caffe_op, "group", param.group)
    # Get dilation - not tested. If you have a model and this checks out,
    # please provide a test and uncomment this.
    if len(param.dilation) > 0:
        if len(param.dilation) == 1:
            AddArgument(caffe_op, "dilation", param.dilation[0])
        elif len(param.dilation) == 2:
            AddArgument(caffe_op, "dilation_h", param.dilation[0])
            AddArgument(caffe_op, "dilation_w", param.dilation[1])
    return caffe_op, params
