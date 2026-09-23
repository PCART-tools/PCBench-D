def find_inputs(module):
    return [n for n in module.graph.nodes if n.op == "placeholder"]
