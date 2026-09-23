def gen_transitive_closure_str(dep_graph: DepGraph, root_ops: List[str]) -> str:
    return ' '.join(gen_transitive_closure(dep_graph, root_ops))
