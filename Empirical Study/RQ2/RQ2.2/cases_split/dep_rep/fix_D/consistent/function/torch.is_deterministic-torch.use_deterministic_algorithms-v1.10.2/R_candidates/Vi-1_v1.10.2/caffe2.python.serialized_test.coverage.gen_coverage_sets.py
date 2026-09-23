def gen_coverage_sets(source_dir):
    covered_ops = gen_covered_ops(source_dir)

    not_covered_ops = set()
    schemaless_ops = []
    for op_name in core._GetRegisteredOperators():
        s = OpSchema.get(op_name)

        if s is not None and s.private:
            continue
        if s:
            if op_name not in covered_ops:
                not_covered_ops.add(op_name)
        else:
            if op_name.find("_ENGINE_") == -1:
                schemaless_ops.append(op_name)
    return (covered_ops, not_covered_ops, schemaless_ops)
