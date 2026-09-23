def is_nested_int(s: Union[int, SymInt]) -> TypeGuard[SymInt]:
    return isinstance(s, torch.SymInt) and s.node.is_nested_int()
