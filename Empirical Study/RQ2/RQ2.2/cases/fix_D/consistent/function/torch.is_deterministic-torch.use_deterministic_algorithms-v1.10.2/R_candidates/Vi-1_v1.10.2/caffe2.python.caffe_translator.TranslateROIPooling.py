@TranslatorRegistry.Register("ROIPooling")
def TranslateROIPooling(layer, pretrained_blobs, is_test, **kwargs):
    caffe_op = BaseTranslate(layer, "RoIPool")
    AddArgument(caffe_op, "order", "NCHW")

    if is_test:
        AddArgument(caffe_op, "is_test", is_test)
    else:
        # Only used for gradient computation
        caffe_op.output.append(caffe_op.output[0] + '_argmaxes')

    param = layer.roi_pooling_param
    if param.HasField('pooled_h'):
        AddArgument(caffe_op, 'pooled_h', param.pooled_h)
    if param.HasField('pooled_w'):
        AddArgument(caffe_op, 'pooled_w', param.pooled_w)
    if param.HasField('spatial_scale'):
        AddArgument(caffe_op, 'spatial_scale', param.spatial_scale)

    return caffe_op, []
