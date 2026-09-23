@register_inference_rule(torch.full)
def full_inference_rule(n: Node, symbols, constraints, counter):
    full, counter = gen_tvar(counter)
    symbols[n] = full
    res = []

    assert isinstance(n.args[0], Iterable)
    for arg in n.args[0]:
        dim = arg if isinstance(arg, int) else symbols[arg]
        res.append(dim)
    c = BinConstraintT(full, TensorType(list(res)), op_eq)  # type: ignore[arg-type]
    return [c], counter
