@TranslatorRegistry.Register("Softmax")
def TranslateSoftmax(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "Softmax")
    return caffe_op, []
