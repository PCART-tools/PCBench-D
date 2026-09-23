def is_symbolic(
    val: Union[int, SymInt, float, SymFloat, bool, SymBool],
) -> TypeGuard[Union[SymInt, SymFloat, SymBool]]:
    if isinstance(val, (int, float, bool)):
        return False
    return val.node.is_symbolic()
