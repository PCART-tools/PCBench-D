def gen_broadcasting_constraints(e1, e2, symbols, counter, output_var):
    # additional vars that don't correspond to expressions
    e11, counter = gen_tvar(counter)
    e22, counter = gen_tvar(counter)

    # generate constraints
    c1 = TGreatestUpperBound(output_var, e11, e22)
    c2 = ApplyBroadcasting(e11, e22, e1, e2)
    c3 = BinConstraintT(e11, e22, op_consistency)
    return [c1, c2, c3], counter
