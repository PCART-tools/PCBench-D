@TranslatorRegistry.Register("LRN")
def TranslateLRN(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "LRN")
    caffe_op.output.extend(['_' + caffe_op.output[0] + '_scale'])
    param = layer.lrn_param
    if param.norm_region != caffe_pb2.LRNParameter.ACROSS_CHANNELS:
        raise ValueError(
            "Does not support norm region other than across channels.")
    AddArgument(caffe_op, "size", int(param.local_size))
    AddArgument(caffe_op, "alpha", float(param.alpha))
    AddArgument(caffe_op, "beta", float(param.beta))
    AddArgument(caffe_op, "bias", float(param.k))
    AddArgument(caffe_op, "order", "NCHW")
    return caffe_op, []
