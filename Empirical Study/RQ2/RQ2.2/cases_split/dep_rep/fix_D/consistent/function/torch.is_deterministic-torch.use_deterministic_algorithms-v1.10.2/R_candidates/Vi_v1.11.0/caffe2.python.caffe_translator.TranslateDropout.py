@TranslatorRegistry.Register("Dropout")
def TranslateDropout(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "Dropout")
    caffe_op.output.extend(['_' + caffe_op.output[0] + '_mask'])
    param = layer.dropout_param
    AddArgument(caffe_op, "ratio", param.dropout_ratio)
    if (is_test):
        AddArgument(caffe_op, "is_test", 1)
    return caffe_op, []
