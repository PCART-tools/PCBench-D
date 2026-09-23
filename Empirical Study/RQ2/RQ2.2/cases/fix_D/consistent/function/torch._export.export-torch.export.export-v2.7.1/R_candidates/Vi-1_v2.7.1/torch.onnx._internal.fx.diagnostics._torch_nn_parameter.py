@_format_argument.register
def _torch_nn_parameter(obj: torch.nn.Parameter) -> str:
    return f"Parameter({format_argument(obj.data)})"
