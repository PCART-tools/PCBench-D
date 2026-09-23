@TranslatorRegistry.Register("BatchNorm")
def TranslateBatchNorm(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "SpatialBN")
    output = caffe_op.output[0]
    param = layer.batch_norm_param
    AddArgument(caffe_op, "is_test", is_test)
    AddArgument(caffe_op, "epsilon", param.eps)
    AddArgument(caffe_op, "order", "NCHW")

    caffe_op.input.extend(
        [output + "_scale",
         output + "_bias",
         output + "_mean",
         output + "_var"])
    if not is_test:
        caffe_op.output.extend(
            [output + "_mean",
             output + "_var",
             output + "_saved_mean",
             output + "_saved_var"])

    n_channels = pretrained_blobs[0].shape[0]
    if pretrained_blobs[2][0] != 0:
        mean = utils.NumpyArrayToCaffe2Tensor(
            (1. / pretrained_blobs[2][0]) * pretrained_blobs[0],
            output + '_mean')
        var = utils.NumpyArrayToCaffe2Tensor(
            (1. / pretrained_blobs[2][0]) * pretrained_blobs[1],
            output + '_var')
    else:
        raise RuntimeError("scalar is zero.")
    if len(pretrained_blobs) > 3:
        # IntelCaffe and NVCaffe uses fused BN+Scale,
        # three blobs for BN and two blobs for Scale,
        # so that the total number of blobs becomes five (including scale and bias).
        scale = utils.NumpyArrayToCaffe2Tensor(
            pretrained_blobs[3].flatten(),
            output + '_scale')
        bias = utils.NumpyArrayToCaffe2Tensor(
            pretrained_blobs[4].flatten(),
            output + '_bias')
    else:
        pretrained_blobs[2][0] = 1
        pretrained_blobs[2] = np.tile(pretrained_blobs[2], (n_channels, ))
        scale = utils.NumpyArrayToCaffe2Tensor(
            pretrained_blobs[2],
            output + '_scale')
        bias = utils.NumpyArrayToCaffe2Tensor(
            np.zeros_like(pretrained_blobs[2]),
            output + '_bias')

    return caffe_op, [scale, bias, mean, var]
