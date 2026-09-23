@TranslatorRegistry.Register("Crop")
def TranslateCrop(layer, pretrained_blobs, is_test, **kwargs):
    net, net_params, input_dims = kwargs['net'], kwargs['net_params'], kwargs['input_dims']
    n, c, h, w = input_dims
    dummy_input = np.random.randn(n, c, h, w).astype(np.float32)
    dim_map = _GetBlobDimMap(net, net_params, dummy_input)
    param = layer.crop_param
    axis, offsets = param.axis, param.offset
    caffe_op = BaseTranslate(layer, "Slice")
    input_1 = caffe_op.input[1]
    input_1_dim = dim_map[input_1]
    starts, ends = [], []
    dims = len(dim_map[input_1])
    assert len(offsets) == 1, 'Caffe Translator for Crop only works for offset \
    of 1 for now'
    for _ in range(axis):
        starts.append(0)
        ends.append(-1)
    end_offset = [int(offsets[0] + input_1_dim[i]) for i in range(axis, dims)]
    ends.extend(end_offset)
    starts.extend([offsets[0]] * len(end_offset))
    op = caffe2_pb2.OperatorDef()
    op.input.extend([caffe_op.input[0]])
    op.output.extend(caffe_op.output)
    op.arg.extend(caffe_op.arg)
    op.type = caffe_op.type
    AddArgument(op, "starts", starts)
    AddArgument(op, "ends", ends)
    return op, []
