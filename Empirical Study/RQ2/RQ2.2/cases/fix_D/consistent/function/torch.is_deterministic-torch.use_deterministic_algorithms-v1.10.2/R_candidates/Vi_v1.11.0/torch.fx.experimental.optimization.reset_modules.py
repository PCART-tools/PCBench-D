def reset_modules(nodes: List[fx.Node], modules: Dict[str, nn.Module], old_modules: Dict[nn.Module, nn.Module]):
    """
    Maps each module that's been changed with `modules_to_mkldnn` back to its
    original.
    """
    for node in nodes:
        if node.op == 'call_module':
            assert(isinstance(node.target, str))
            cur_module = modules[node.target]
            if cur_module in old_modules:
                replace_node_module(node, modules, old_modules[cur_module])
