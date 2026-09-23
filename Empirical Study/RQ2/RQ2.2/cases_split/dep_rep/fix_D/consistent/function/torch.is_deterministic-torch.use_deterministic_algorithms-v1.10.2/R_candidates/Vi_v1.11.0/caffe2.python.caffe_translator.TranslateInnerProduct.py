@TranslatorRegistry.Register("InnerProduct")
def TranslateInnerProduct(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.inner_product_param
    try:
        if param.axis != 1 or param.transpose:
            raise ValueError(
                "We don't have testing case for non-default axis and transpose "
                "cases yet so we are disabling it for now. If you have a model "
                "with this, please do send us your model for us to update this "
                "support, and you are more than welcome to send a PR for this.")
    except AttributeError:
        # We might be using an historic Caffe protobuf that does not have axis
        # and transpose arguments, so we will silently pass.
        pass
    caffe_op = BaseTranslate(layer, "FC")
    output = caffe_op.output[0]
    caffe_op.input.extend([output + '_w', output + '_b'])
    # To provide the old-style 4-dimensional blob (1, 1, dim_output, dim_input)
    # case, we always explicitly reshape the pretrained blob.
    if pretrained_blobs[0].ndim not in [2, 4]:
        raise ValueError("Unexpected weight ndim.")
    if (pretrained_blobs[0].ndim == 4 and
            list(pretrained_blobs[0].shape[:2]) != [1, 1]):
        raise ValueError(
            "If pretrained blob has 4 dims (old-style Caffe), the first two "
            "should be of value 1, but I got " + str(pretrained_blobs[0].shape))
    weight = utils.NumpyArrayToCaffe2Tensor(
        pretrained_blobs[0].reshape(-1, pretrained_blobs[0].shape[-1]),
        output + '_w'
    )
    bias = utils.NumpyArrayToCaffe2Tensor(
        pretrained_blobs[1].flatten(), output + '_b'
    )
    return caffe_op, [weight, bias]
