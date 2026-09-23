@register_inference_rule(torch.nn.functional.embedding)
def embedding_inference_rule_functional(n: Node, symbols, constraints, counter):
    assert isinstance(n.args[0], Node)

    embedding_dim_weights = symbols[n.args[1]]

    # will treat this as a static shape. So we will not use matching.
    weight_dims, counter = gen_tensor_dims(2, counter)
    equality_constraint = BinConstraintT(
        embedding_dim_weights, TensorType(weight_dims), op_eq
    )
    embedding_dim = weight_dims[1]
    constraints, counter = gen_embedding_rules(n, symbols, embedding_dim, counter)
    return [equality_constraint] + constraints, counter
