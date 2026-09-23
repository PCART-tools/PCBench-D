@TranslatorRegistry.Register("PReLU")
def TranslatePRelu(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "PRelu")
    output = caffe_op.output[0]
    caffe_op.input.extend([output + '_Slope'])
    slope = utils.NumpyArrayToCaffe2Tensor(pretrained_blobs[0], output + '_Slope')

    return caffe_op, [slope]
