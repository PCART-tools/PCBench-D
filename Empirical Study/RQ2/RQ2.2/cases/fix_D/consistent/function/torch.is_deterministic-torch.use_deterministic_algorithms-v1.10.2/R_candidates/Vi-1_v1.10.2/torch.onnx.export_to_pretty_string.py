def export_to_pretty_string(*args, **kwargs) -> str:
    r"""
    Similar to :func:`export`, but returns a text representation of the ONNX
    model. Only differences in args listed below. All other args are the same
    as :func:`export`.

    Args:
      f:  Deprecated and ignored. Will be removed in the next release of
          PyTorch.
      add_node_names (bool, default True): Whether or not to set
          NodeProto.name. This makes no difference unless
          ``google_printer=True``.
      google_printer (bool, default False): If False, will return a custom,
          compact representation of the model. If True will return the
          protobuf's `Message::DebugString()`, which is more verbose.

    Returns:
      A UTF-8 str containing a human-readable representation of the ONNX model.
    """
    from torch.onnx import utils
    return utils.export_to_pretty_string(*args, **kwargs)
