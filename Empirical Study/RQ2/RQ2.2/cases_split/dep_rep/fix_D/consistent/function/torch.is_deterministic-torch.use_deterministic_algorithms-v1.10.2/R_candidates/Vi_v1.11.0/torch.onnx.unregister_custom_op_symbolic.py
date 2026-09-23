def unregister_custom_op_symbolic(symbolic_name, opset_version):
    r"""
    Unregisters ``symbolic_name``. See
    "Custom Operators" in the module documentation for an example usage.

    Args:
      symbolic_name (str): The name of the custom operator in "<domain>::<op>"
        format.
      opset_version (int): The ONNX opset version in which to unregister.
    """

    from torch.onnx import utils
    utils.unregister_custom_op_symbolic(symbolic_name, opset_version)
