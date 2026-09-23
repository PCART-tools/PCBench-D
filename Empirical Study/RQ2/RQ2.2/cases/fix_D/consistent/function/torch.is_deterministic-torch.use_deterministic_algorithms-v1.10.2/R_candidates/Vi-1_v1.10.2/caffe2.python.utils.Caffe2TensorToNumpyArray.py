def Caffe2TensorToNumpyArray(tensor):
    if tensor.data_type == caffe2_pb2.TensorProto.FLOAT:
        return np.asarray(
            tensor.float_data, dtype=np.float32).reshape(tensor.dims)
    elif tensor.data_type == caffe2_pb2.TensorProto.DOUBLE:
        return np.asarray(
            tensor.double_data, dtype=np.float64).reshape(tensor.dims)
    elif tensor.data_type == caffe2_pb2.TensorProto.INT64:
        return np.asarray(
            tensor.int64_data, dtype=np.int64).reshape(tensor.dims)
    elif tensor.data_type == caffe2_pb2.TensorProto.INT32:
        return np.asarray(
            tensor.int32_data, dtype=np.int).reshape(tensor.dims)   # pb.INT32=>np.int use int32_data
    elif tensor.data_type == caffe2_pb2.TensorProto.INT16:
        return np.asarray(
            tensor.int32_data, dtype=np.int16).reshape(tensor.dims)  # pb.INT16=>np.int16 use int32_data
    elif tensor.data_type == caffe2_pb2.TensorProto.UINT16:
        return np.asarray(
            tensor.int32_data, dtype=np.uint16).reshape(tensor.dims)  # pb.UINT16=>np.uint16 use int32_data
    elif tensor.data_type == caffe2_pb2.TensorProto.INT8:
        return np.asarray(
            tensor.int32_data, dtype=np.int8).reshape(tensor.dims)  # pb.INT8=>np.int8 use int32_data
    elif tensor.data_type == caffe2_pb2.TensorProto.UINT8:
        return np.asarray(
            tensor.int32_data, dtype=np.uint8).reshape(tensor.dims)  # pb.UINT8=>np.uint8 use int32_data
    else:
        # TODO: complete the data type: bool, float16, byte, int64, string
        raise RuntimeError(
            "Tensor data type not supported yet: " + str(tensor.data_type))
