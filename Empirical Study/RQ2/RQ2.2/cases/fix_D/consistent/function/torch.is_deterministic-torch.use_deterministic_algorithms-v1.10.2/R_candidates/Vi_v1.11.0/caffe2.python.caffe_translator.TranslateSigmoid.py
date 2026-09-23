@TranslatorRegistry.Register("Sigmoid")
def TranslateSigmoid(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "Sigmoid")
    return caffe_op, []
