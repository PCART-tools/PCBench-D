@register_inference_rule(torch._C._nn.linear)
def torch_linear_inference_rule(n: Node, symbols, constraints, counter):
    assert isinstance(n.args[0], Node)
    weight_dims, counter = gen_tensor_dims(2, counter)
    equality_constraint = BinConstraintT(
        symbols[n.args[1]], TensorType(weight_dims), op_eq
    )
    constraints, counter = linear_constraints(
        n, weight_dims[1], weight_dims[0], symbols, counter
    )
    return [equality_constraint] + constraints, counter
