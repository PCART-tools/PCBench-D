def _is_onnx_list(value):
    if not isinstance(value, string_classes) and \
            not isinstance(value, torch.Tensor) and \
            isinstance(value, collections.abc.Iterable):
        return True
    return False
