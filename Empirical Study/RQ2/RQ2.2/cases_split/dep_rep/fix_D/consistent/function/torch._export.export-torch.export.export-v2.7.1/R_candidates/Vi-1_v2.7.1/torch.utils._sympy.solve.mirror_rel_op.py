def mirror_rel_op(type: type) -> Optional[type[sympy.Rel]]:
    return _MIRROR_REL_OP.get(type, None)
