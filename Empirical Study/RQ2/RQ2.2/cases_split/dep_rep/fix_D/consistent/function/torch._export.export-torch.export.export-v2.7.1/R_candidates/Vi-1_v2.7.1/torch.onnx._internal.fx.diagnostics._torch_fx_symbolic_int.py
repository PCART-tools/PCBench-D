@_format_argument.register
def _torch_fx_symbolic_int(obj: torch.SymInt) -> str:
    return f"SymInt({obj})"
