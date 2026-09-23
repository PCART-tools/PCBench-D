def add_linear_constraints(dims1, dims2, in_features, out_features):
    assert len(dims1) == len(dims2)
    constraints = []
    for i in range(len(dims1)):
        if i == len(dims1) - 1:
            constraints.append(BinConstraintD(dims1[i], in_features, op_consistency))
            constraints.append(BinConstraintD(dims2[i], out_features, op_eq))
        else:
            constraints.append(BinConstraintD(dims1[i], dims2[i], op_eq))

    return constraints
