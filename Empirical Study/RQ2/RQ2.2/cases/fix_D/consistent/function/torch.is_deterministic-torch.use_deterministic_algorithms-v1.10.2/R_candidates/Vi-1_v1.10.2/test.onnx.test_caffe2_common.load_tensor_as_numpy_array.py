def load_tensor_as_numpy_array(f):
    tensor = onnx.TensorProto()
    with open(f, "rb") as file:
        tensor.ParseFromString(file.read())
    return tensor
