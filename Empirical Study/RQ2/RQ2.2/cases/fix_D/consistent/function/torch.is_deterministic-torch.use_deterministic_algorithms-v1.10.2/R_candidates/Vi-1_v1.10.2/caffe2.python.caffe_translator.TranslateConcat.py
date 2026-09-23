@TranslatorRegistry.Register("Concat")
def TranslateConcat(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "Concat")
    caffe_op.output.extend(['_' + caffe_op.output[0] + '_dims'])
    AddArgument(caffe_op, "order", "NCHW")
    return caffe_op, []
