@_format_argument.register
def _torch_nn_module(obj: torch.nn.Module) -> str:
    return f"torch.nn.Module({obj.__class__.__name__})"
