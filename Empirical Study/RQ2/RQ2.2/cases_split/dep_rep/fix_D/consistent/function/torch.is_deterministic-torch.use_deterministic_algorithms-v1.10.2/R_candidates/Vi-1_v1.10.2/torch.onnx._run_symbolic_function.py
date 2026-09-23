def _run_symbolic_function(*args, **kwargs):
    from torch.onnx import utils
    return utils._run_symbolic_function(*args, **kwargs)
