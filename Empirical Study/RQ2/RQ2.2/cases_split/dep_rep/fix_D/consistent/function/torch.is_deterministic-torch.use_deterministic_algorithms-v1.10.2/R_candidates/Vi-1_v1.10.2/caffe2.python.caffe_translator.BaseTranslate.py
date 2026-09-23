def BaseTranslate(layer, caffe2_type):
    """A simple translate interface that maps the layer input and output."""
    caffe2_op = caffe2_pb2.OperatorDef()
    caffe2_op.type = caffe2_type
    caffe2_op.input.extend(layer.bottom)
    caffe2_op.output.extend(layer.top)
    return caffe2_op
