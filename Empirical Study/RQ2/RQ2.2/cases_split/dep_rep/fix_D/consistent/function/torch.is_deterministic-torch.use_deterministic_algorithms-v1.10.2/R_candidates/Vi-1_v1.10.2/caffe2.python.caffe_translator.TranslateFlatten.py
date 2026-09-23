@TranslatorRegistry.Register("Flatten")
def TranslateFlatten(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.flatten_param
    if param.end_axis != -1:
        raise NotImplementedError("flatten_param.end_axis not supported yet.")

    if param.axis == 0:
        caffe_op = BaseTranslate(layer, "FlattenToVec")
    elif param.axis == 1:
        caffe_op = BaseTranslate(layer, "Flatten")
    else:
        # This could be a Reshape op, but dim size is not known here.
        raise NotImplementedError(
            "Not supported yet for flatten_param.axis {}.".format(param.axis))

    return caffe_op, []
