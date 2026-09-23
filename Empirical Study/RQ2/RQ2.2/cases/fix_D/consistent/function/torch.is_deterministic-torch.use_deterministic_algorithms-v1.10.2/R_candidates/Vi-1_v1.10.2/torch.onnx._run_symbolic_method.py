def _run_symbolic_method(*args, **kwargs):
    from torch.onnx import utils
    return utils._run_symbolic_method(*args, **kwargs)
