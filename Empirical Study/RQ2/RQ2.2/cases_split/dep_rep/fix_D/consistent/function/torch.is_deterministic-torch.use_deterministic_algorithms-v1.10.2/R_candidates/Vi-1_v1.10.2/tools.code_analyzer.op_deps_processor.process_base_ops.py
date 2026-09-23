def process_base_ops(graph: Any, base_ops: List[str]) -> None:
    # remove base ops from all `depends` lists to compress the output graph
    for op in graph:
        op['depends'] = [
            dep for dep in op.get('depends', []) if dep['name'] not in base_ops
        ]

    # add base ops section at the beginning
    graph.insert(0, {
        'name': '__BASE__',
        'depends': [{'name': name} for name in base_ops]})
