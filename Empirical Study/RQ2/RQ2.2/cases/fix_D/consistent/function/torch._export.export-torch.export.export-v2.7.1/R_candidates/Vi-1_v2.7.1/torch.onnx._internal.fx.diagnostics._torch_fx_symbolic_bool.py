@_format_argument.register
def _torch_fx_symbolic_bool(obj: torch.SymBool) -> str:
    return f"SymBool({obj})"
