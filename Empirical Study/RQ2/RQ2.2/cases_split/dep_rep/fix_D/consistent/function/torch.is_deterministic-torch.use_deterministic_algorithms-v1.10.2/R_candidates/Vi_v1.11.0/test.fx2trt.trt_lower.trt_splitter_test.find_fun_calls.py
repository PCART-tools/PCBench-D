def find_fun_calls(module, target):
    return [
        n for n in module.graph.nodes if n.op == "call_function" and n.target == target
    ]
