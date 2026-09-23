def load_op_dep_graph(fname: str) -> DepGraph:
    with open(fname, 'r') as stream:
        result = defaultdict(set)
        for op in yaml.safe_load(stream):
            op_name = canonical_name(op['name'])
            for dep in op.get('depends', []):
                dep_name = canonical_name(dep['name'])
                result[op_name].add(dep_name)
        return dict(result)
