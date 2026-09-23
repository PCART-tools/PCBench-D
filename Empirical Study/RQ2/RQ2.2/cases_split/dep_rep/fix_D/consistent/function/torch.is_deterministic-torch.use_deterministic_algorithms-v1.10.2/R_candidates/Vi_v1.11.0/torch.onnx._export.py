def _export(*args, **kwargs):
    from torch.onnx import utils
    result = utils._export(*args, **kwargs)
    return result
