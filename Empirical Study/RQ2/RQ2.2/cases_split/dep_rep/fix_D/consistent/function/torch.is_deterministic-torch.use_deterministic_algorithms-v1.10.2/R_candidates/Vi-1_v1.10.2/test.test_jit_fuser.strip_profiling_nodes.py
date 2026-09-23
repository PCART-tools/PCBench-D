def strip_profiling_nodes(nodes):
    profiling_opcodes = set(['prim::BailoutTemplate', 'prim::BailOut'])
    return [n for n in nodes if n.kind() not in profiling_opcodes]
