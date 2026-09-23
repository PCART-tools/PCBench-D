def is_in_onnx_export():
    r"""
    Returns True iff :func:`export` is running in the current thread
    """

    from torch.onnx import utils
    return utils.is_in_onnx_export()
