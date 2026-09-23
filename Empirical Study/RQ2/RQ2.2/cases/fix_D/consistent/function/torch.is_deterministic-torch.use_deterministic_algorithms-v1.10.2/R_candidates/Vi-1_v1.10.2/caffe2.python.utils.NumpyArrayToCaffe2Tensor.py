def NumpyArrayToCaffe2Tensor(arr, name=None):
    tensor = caffe2_pb2.TensorProto()
    tensor.dims.extend(arr.shape)
    if name:
        tensor.name = name
    if arr.dtype == np.float32:
        tensor.data_type = caffe2_pb2.TensorProto.FLOAT
        tensor.float_data.extend(list(arr.flatten().astype(float)))
    elif arr.dtype == np.float64:
        tensor.data_type = caffe2_pb2.TensorProto.DOUBLE
        tensor.double_data.extend(list(arr.flatten().astype(np.float64)))
    elif arr.dtype == np.int64:
        tensor.data_type = caffe2_pb2.TensorProto.INT64
        tensor.int64_data.extend(list(arr.flatten().astype(np.int64)))
    elif arr.dtype == np.int or arr.dtype == np.int32:
        tensor.data_type = caffe2_pb2.TensorProto.INT32
        tensor.int32_data.extend(arr.flatten().astype(np.int).tolist())
    elif arr.dtype == np.int16:
        tensor.data_type = caffe2_pb2.TensorProto.INT16
        tensor.int32_data.extend(list(arr.flatten().astype(np.int16)))  # np.int16=>pb.INT16 use int32_data
    elif arr.dtype == np.uint16:
        tensor.data_type = caffe2_pb2.TensorProto.UINT16
        tensor.int32_data.extend(list(arr.flatten().astype(np.uint16)))  # np.uint16=>pb.UNIT16 use int32_data
    elif arr.dtype == np.int8:
        tensor.data_type = caffe2_pb2.TensorProto.INT8
        tensor.int32_data.extend(list(arr.flatten().astype(np.int8)))   # np.int8=>pb.INT8 use int32_data
    elif arr.dtype == np.uint8:
        tensor.data_type = caffe2_pb2.TensorProto.UINT8
        tensor.int32_data.extend(list(arr.flatten().astype(np.uint8)))   # np.uint8=>pb.UNIT8 use int32_data
    else:
        # TODO: complete the data type: bool, float16, byte, string
        raise RuntimeError(
            "Numpy data type not supported yet: " + str(arr.dtype))
    return tensor
