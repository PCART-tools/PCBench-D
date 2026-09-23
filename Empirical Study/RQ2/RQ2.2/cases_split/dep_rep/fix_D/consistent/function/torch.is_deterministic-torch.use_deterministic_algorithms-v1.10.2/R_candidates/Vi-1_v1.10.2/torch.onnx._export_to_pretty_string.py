def _export_to_pretty_string(*args, **kwargs):
    from torch.onnx import utils
    return utils._export_to_pretty_string(*args, **kwargs)
