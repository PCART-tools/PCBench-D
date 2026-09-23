def cast_symbool_to_symint_guardless(
    symbool: Union[bool, torch.SymBool]
) -> Union[int, torch.SymInt]:
    if isinstance(symbool, bool):
        return 1 if symbool else 0
    int_sym = _sympy_cast_symbool_to_symint_guardless(symbool.node.expr)
    return symbool.node.shape_env.create_symintnode(
        int_sym, hint=int(symbool.node.require_hint()) if has_hint(symbool) else None
    )
