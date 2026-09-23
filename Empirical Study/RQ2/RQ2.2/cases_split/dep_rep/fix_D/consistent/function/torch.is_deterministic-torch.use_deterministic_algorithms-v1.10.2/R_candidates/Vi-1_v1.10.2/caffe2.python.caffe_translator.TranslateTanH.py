@TranslatorRegistry.Register("TanH")
def TranslateTanH(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "Tanh")
    return caffe_op, []
