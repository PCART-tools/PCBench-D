def extract_all_operators(selective_builder: SelectiveBuilder) -> Set[str]:
    ops = []
    for (op_name, op) in selective_builder.operators.items():
        ops.append(op_name)
    return set(ops)
