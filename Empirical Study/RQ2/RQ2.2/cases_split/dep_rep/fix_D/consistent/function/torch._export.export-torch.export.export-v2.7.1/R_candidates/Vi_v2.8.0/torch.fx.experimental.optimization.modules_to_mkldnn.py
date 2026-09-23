def modules_to_mkldnn(nodes: list[fx.Node], modules: dict[str, nn.Module]):
    """
    For each node, if it's a module that can be preconverted into MKLDNN,
    then we do so and create a mapping to allow us to convert from the MKLDNN
    version of the module to the original.
    """
    old_modules: dict[nn.Module, nn.Module] = {}
    for node in nodes:
        if node.op == "call_module":
            assert isinstance(node.target, str)
            cur_module = modules[node.target]
            if type(cur_module) in mkldnn_map:
                new_module = mkldnn_map[type(cur_module)](cur_module, torch.float)
                assert isinstance(new_module, nn.Module)
                old_modules[new_module] = copy.deepcopy(cur_module)
                replace_node_module(node, modules, new_module)
    return old_modules
