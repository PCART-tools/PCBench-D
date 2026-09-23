def convert(
    fname: str,
    graph: Any,
    output_template: CodeTemplate,
    op_template: CodeTemplate,
    op_dep_template: CodeTemplate,
) -> None:
    ops = []
    for op in graph:
        op_name = op['name']
        op_deps = []

        for dep in op.get('depends', []):
            dep_name = dep['name']
            if dep_name == op_name:
                # skip itself reference
                continue
            op_deps.append(
                op_dep_template.substitute(
                    op_name=op_name,
                    dep_name=dep_name))

        if not op_deps:
            # skip ops without any fanout
            continue

        ops.append(
            op_template.substitute(
                op_name=op_name,
                op_deps=op_deps))

    with open(fname, 'w') as out:
        out.write(output_template.substitute(ops=ops))
