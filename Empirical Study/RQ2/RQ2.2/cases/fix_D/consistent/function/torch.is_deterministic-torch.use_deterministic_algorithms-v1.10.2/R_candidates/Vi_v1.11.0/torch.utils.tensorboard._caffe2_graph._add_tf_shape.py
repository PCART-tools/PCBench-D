def _add_tf_shape(attr_dict, ints):
    '''
    Converts a list of ints to a TensorShapeProto representing the dimensions of
    a blob/object.

    Args:
        attr_dict: Dictionary to update (usually attributes of a Node)
        ints: List of integers representing dimensions of some object.

    Returns:
        None. Modifies attr_dict in-place.
    '''
    shape_proto = TensorShapeProto()
    for i in ints:
        dim = TensorShapeProto.Dim()
        dim.size = i
        shape_proto.dim.extend([dim])
    attr_dict['_output_shapes'].list.shape.extend([shape_proto])
