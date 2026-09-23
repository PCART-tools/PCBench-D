def from_python_type_to_onnx_tensor_element_type(type: type):
    """
    Converts a Python type to the corresponding ONNX tensor element type.
    For example, `from_python_type_to_onnx_tensor_element_type(float)` returns
    `onnx.TensorProto.FLOAT`.

    Args:
      type (type): The Python type to convert.

    Returns:
      int: The corresponding ONNX tensor element type.

    """
    _PYTHON_TYPE_TO_ONNX_TENSOR_ELEMENT_TYPE = {
        float: onnx.TensorProto.FLOAT,  # type: ignore[attr-defined]
        int: onnx.TensorProto.INT64,  # type: ignore[attr-defined]
        bool: onnx.TensorProto.BOOL,  # type: ignore[attr-defined]
    }
    return _PYTHON_TYPE_TO_ONNX_TENSOR_ELEMENT_TYPE.get(type)
