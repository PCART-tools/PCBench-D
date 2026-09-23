@_format_argument.register
def _torch_fx_symbolic_float(obj: torch.SymFloat) -> str:
    return f"SymFloat({obj})"
