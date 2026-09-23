def register_custom_op_symbolic(symbolic_name, symbolic_fn, opset_version):
    r"""
    Registers ``symbolic_fn`` to handle ``symbolic_name``. See
    "Custom Operators" in the module documentation for an example usage.

    Args:
      symbolic_name (str): The name of the custom operator in "<domain>::<op>"
        format.
      symbolic_fn (Callable): A function that takes in the ONNX graph and
        the input arguments to the current operator, and returns new
        operator nodes to add to the graph.
      opset_version (int): The ONNX opset version in which to register.
    """
    from torch.onnx import utils
    utils.register_custom_op_symbolic(symbolic_name, symbolic_fn, opset_version)
