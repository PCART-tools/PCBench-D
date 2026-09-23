def extract_root_operators(selective_builder: SelectiveBuilder) -> Set[str]:
    ops = []
    for (op_name, op) in selective_builder.operators.items():
        if op.is_root_operator:
            ops.append(op_name)
    return set(ops)
