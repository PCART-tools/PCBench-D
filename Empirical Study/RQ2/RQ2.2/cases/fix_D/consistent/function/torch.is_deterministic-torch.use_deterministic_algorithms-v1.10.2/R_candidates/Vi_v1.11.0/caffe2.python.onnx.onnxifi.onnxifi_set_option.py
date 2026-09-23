def onnxifi_set_option(option_name, option_value):
    """
    Set onnxifi option
    """
    return C.onnxifi_set_option(option_name, str(option_value))
