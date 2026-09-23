def tensor_shape_proto(outputsize):
    """Creates an object matching
    https://github.com/tensorflow/tensorboard/blob/master/tensorboard/compat/proto/tensor_shape.proto
    """
    return TensorShapeProto(dim=[TensorShapeProto.Dim(size=d) for d in outputsize])
