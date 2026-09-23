def find_output(module):
    return next(n for n in module.graph.nodes if n.op == "output")
