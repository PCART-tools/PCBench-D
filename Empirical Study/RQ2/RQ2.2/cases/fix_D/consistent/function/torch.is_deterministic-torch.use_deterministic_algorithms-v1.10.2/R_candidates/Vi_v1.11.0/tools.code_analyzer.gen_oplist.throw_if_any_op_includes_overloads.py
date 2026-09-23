def throw_if_any_op_includes_overloads(selective_builder: SelectiveBuilder) -> None:
    ops = []
    for (op_name, op) in selective_builder.operators.items():
        if op.include_all_overloads:
            ops.append(op_name)
    if ops:
        raise Exception(
            (
                "Operators that include all overloads are "
                + "not allowed since --allow_include_all_overloads "
                + "was specified: {}"
            ).format(", ".join(ops))
        )
