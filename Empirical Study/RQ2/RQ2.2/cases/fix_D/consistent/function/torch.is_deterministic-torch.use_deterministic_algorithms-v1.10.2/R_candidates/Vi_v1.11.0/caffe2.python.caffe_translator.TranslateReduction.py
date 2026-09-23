@TranslatorRegistry.Register("Reduction")
def TranslateReduction(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.reduction_param
    if param.operation == caffe_pb2.ReductionParameter.SUM:
        caffe_op = BaseTranslate(layer, "ReduceBackSum")
    elif param.operation == caffe_pb2.ReductionParameter.MEAN:
        caffe_op = BaseTranslate(layer, "ReduceBackMean")
    else:
        raise NotImplementedError("Not yet supported")

    if param.axis > 0:
        # We can't figure out the number of dims to reduce from positive axis
        # for back reduction since the shape info is not known here.
        raise NotImplementedError("Not yet supported")
    num_reduce_dim = -param.axis
    AddArgument(caffe_op, "num_reduce_dim", num_reduce_dim)

    return caffe_op, []
