@TranslatorRegistry.Register("Pooling3D")
def TranslatePool3D(layer, pretrained_blobs, is_test, **kwargs):
    param = layer.pooling3d_param
    if param.pool == caffe_pb2.Pooling3DParameter.MAX:
        caffe_op = BaseTranslate(layer, "MaxPool")

    elif param.pool == caffe_pb2.Pooling3DParameter.AVE:
        caffe_op = BaseTranslate(layer, "AveragePool")
    AddArgument(caffe_op, "order", "NCHW")
    AddArgument(
        caffe_op,
        "kernels",
        [param.kernel_depth, param.kernel_size, param.kernel_size])

    AddArgument(
        caffe_op,
        "strides",
        [param.temporal_stride, param.stride, param.stride])
    temporal_pad = 0
    spatial_pad = 0
    if hasattr(param, 'temporal_pad'):
        temporal_pad = param.temporal_pad
    if hasattr(param, 'pad'):
        spatial_pad = param.pad
    AddArgument(caffe_op, "pads", [temporal_pad, spatial_pad, spatial_pad] * 2)
    return caffe_op, []
