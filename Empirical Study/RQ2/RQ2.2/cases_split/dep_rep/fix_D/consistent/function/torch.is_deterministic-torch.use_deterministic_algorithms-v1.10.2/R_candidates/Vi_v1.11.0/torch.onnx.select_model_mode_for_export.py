def select_model_mode_for_export(model, mode):
    r"""
    A context manager to temporarily set the training mode of ``model``
    to ``mode``, resetting it when we exit the with-block.  A no-op if
    mode is None.

    Args:
      model: Same type and meaning as ``model`` arg to :func:`export`.
      mode: Same type and meaning as ``training`` arg to :func:`export`.
    """

    from torch.onnx import utils
    return utils.select_model_mode_for_export(model, mode)
