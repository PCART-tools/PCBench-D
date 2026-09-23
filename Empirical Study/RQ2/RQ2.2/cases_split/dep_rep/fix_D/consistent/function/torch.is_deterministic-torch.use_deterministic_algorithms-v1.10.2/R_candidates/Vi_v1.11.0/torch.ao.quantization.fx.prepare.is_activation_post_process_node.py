def is_activation_post_process_node(node: Node, modules: Dict[str, torch.nn.Module]) -> bool:
    return isinstance(node, torch.fx.Node) and node.op == "call_module" and \
        is_activation_post_process(modules[str(node.target)])
