@TranslatorRegistry.Register("Eltwise")
def TranslateElementWise(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.eltwise_param
    # TODO(jiayq): if we have a protobuf that uses this, lift this constraint
    # and verify that we can correctly translate.
    if len(param.coeff) or param.operation != 1:
        raise RuntimeError("This eltwise layer is not yet supported.")
    caffe_op = BaseTranslate(layer, "Sum")
    return caffe_op, []
