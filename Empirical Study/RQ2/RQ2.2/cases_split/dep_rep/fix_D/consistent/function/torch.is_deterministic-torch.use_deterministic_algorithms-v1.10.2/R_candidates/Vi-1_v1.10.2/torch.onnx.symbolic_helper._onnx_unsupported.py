def _onnx_unsupported(op_name):
    raise RuntimeError("Unsupported: ONNX export of operator {}. "
                       "Please feel free to request support or submit a pull request on PyTorch GitHub.".format(op_name))
