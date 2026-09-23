def _CheckDataType():
    # Verify that the DataType values defined above match the ones defined in
    # the caffe2.proto file
    for name, value in caffe2_pb2.TensorProto.DataType.items():
        py_value = getattr(DataType, name, None)
        if py_value != value:
            raise AssertionError(
                f"DataType {name} does not match the value defined in "
                f"caffe2.proto: {py_value} vs {value}"
            )
