@TranslatorRegistry.Register("InstanceNorm")
def TranslateInstanceNorm(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "InstanceNorm")
    output = caffe_op.output[0]
    weight = utils.NumpyArrayToCaffe2Tensor(
        pretrained_blobs[0].flatten(), output + '_w')
    bias = utils.NumpyArrayToCaffe2Tensor(
        pretrained_blobs[1].flatten(), output + '_b')
    caffe_op.input.extend([output + '_w', output + '_b'])
    AddArgument(caffe_op, "order", "NCHW")
    return caffe_op, [weight, bias]
