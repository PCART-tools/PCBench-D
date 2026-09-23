@TranslatorRegistry.Register("Reshape")
def TranslateReshape(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "Reshape")
    caffe_op.output.append("_" + caffe_op.input[0] + "_dims")
    reshape_param = layer.reshape_param
    AddArgument(caffe_op, 'shape', reshape_param.shape.dim)
    return caffe_op, []
