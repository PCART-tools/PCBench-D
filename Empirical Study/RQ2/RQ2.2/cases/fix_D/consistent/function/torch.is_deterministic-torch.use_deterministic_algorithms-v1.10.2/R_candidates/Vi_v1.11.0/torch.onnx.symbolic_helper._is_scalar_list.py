def _is_scalar_list(x):
    """
    Check if x is a scalar list, for example: List[float], List[int].

    Besides checking the type is ListType, we also check if the data type is
    a valid ONNX data type.
    """
    element_type = str(x.type().getElementType())
    return _is_list(x) and \
        element_type in scalar_name_to_pytorch.keys() and \
        (scalar_name_to_pytorch[element_type] in cast_pytorch_to_onnx.keys())
