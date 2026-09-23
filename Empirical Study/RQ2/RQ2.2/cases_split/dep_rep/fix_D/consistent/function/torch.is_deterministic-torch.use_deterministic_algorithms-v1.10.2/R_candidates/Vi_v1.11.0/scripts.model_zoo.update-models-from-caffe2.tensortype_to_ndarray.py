def tensortype_to_ndarray(tensor_type):
    shape = []
    for dim in tensor_type.shape.dim:
        shape.append(dim.dim_value)
    if tensor_type.elem_type == onnx.TensorProto.FLOAT:
        type = np.float32
    elif tensor_type.elem_type == onnx.TensorProto.INT:
        type = np.int32
    else:
        raise
    array = np.random.rand(*shape).astype(type)
    return array
