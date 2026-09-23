@TranslatorRegistry.Register("Accuracy")
def TranslateAccuracy(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "Accuracy")
    if layer.accuracy_param.top_k != 1:
        AddArgument(caffe_op, "top_k", layer.accuracy_param.top_k)
    return caffe_op, []
