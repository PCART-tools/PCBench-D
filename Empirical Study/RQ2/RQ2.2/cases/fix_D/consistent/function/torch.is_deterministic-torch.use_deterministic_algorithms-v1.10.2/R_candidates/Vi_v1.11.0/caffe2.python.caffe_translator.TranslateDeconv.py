@TranslatorRegistry.Register("Deconvolution")
def TranslateDeconv(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.convolution_param
    if param.group > 1:
        raise NotImplementedError(
            "Translator currently does not support group deconvolution."
        )
    caffe_op = BaseTranslate(layer, "ConvTranspose")
    output = caffe_op.output[0]
    _TranslateStridePadKernelHelper(param, caffe_op)
    caffe_op.input.extend([output + '_w'])
    AddArgument(caffe_op, "order", "NCHW")
    weight = utils.NumpyArrayToCaffe2Tensor(pretrained_blobs[0], output + '_w')
    if param.bias_term:
        bias = utils.NumpyArrayToCaffe2Tensor(
            pretrained_blobs[1].flatten(), output + '_b'
        )
        caffe_op.input.extend([output + '_b'])
        return caffe_op, [weight, bias]
    else:
        return caffe_op, [weight]
