@TranslatorRegistry.Register("ReLU")
def TranslateRelu(layer, pretrained_blobs, is_test, **kwargs):
    return BaseTranslate(layer, "Relu"), []
