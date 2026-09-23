@TranslatorRegistry.Register("Pooling")
def TranslatePool(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.pooling_param
    if param.pool == caffe_pb2.PoolingParameter.MAX:
        caffe_op = BaseTranslate(layer, "MaxPool")
    elif param.pool == caffe_pb2.PoolingParameter.AVE:
        caffe_op = BaseTranslate(layer, "AveragePool")
    _TranslateStridePadKernelHelper(param, caffe_op)
    AddArgument(caffe_op, "order", "NCHW")
    try:
        # In the Facebook port of Caffe, a torch_pooling field was added to
        # map the pooling computation of Torch. Essentially, it uses
        #   floor((height + 2 * padding - kernel) / stride) + 1
        # instead of
        #   ceil((height + 2 * padding - kernel) / stride) + 1
        # which is Caffe's version.
        # Torch pooling is actually the same as Caffe2 pooling, so we don't
        # need to do anything.
        is_torch_pooling = param.torch_pooling
    except AttributeError:
        is_torch_pooling = False
    if not is_torch_pooling:
        AddArgument(caffe_op, "legacy_pad",
                    caffe2_legacy_pb2.CAFFE_LEGACY_POOLING)
    if param.global_pooling:
        AddArgument(caffe_op, "global_pooling", 1)
    return caffe_op, []
