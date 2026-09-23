def _add_tf_shape(m, ints):
    sh = tensor_shape_pb2.TensorShapeProto()
    for i in ints:
        dim = tensor_shape_pb2.TensorShapeProto.Dim()
        dim.size = i
        sh.dim.extend([dim])
    m['_output_shapes'].list.shape.extend([sh])
