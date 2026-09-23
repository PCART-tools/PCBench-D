def is_torch_symbolic_type(value: Any) -> bool:
    return isinstance(value, (torch.SymBool, torch.SymInt, torch.SymFloat))
