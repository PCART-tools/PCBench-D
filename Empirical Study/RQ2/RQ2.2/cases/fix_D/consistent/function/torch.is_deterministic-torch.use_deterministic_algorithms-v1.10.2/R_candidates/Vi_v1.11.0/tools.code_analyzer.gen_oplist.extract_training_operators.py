def extract_training_operators(selective_builder: SelectiveBuilder) -> Set[str]:
    ops = []
    for (op_name, op) in selective_builder.operators.items():
        if op.is_used_for_training:
            ops.append(op_name)
    return set(ops)
