def register_ops_helper(domain, version, iter_version):
    version_ops = get_ops_in_version(iter_version)
    for op in version_ops:
        if op[0] == "_len":
            op = ("len", op[1])
        if op[0] == "_list":
            op = ("list", op[1])
        if op[0] == "_any":
            op = ("any", op[1])
        if op[0] == "_all":
            op = ("all", op[1])
        domain_register = domain
        if op[0].startswith("prim_"):
            op = (op[0][5:], op[1])
            domain_register = "prim"
        if isfunction(op[1]) and not is_registered_op(op[0], domain_register, version):
            register_op(op[0], op[1], domain_register, version)
