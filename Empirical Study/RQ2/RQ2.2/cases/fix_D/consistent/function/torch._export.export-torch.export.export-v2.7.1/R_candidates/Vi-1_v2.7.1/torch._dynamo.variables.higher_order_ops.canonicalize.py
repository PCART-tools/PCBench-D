def canonicalize(gmod, root_gmod):
    # autograd_cache_key is sensitive to the name of the placeholder and intermediate nodes.
    # So, we first canonicalize it.
    new_graph = torch.fx.Graph()
    env = {}

    placeholder_counter = itertools.count(0)

    def next_placeholder_name():
        nonlocal placeholder_counter
        return f"placeholder_{next(placeholder_counter)}"

    node_counter = itertools.count(0)

    def next_node_name():
        nonlocal node_counter
        return f"node_{next(node_counter)}"

    for node in gmod.graph.nodes:
        if node.op == "placeholder":
            env[node] = new_graph.placeholder(next_placeholder_name())
        else:
            # Can't use node_copy because node.name will not be unique.
            args = map_arg(node.args, lambda x: env[x])
            kwargs = map_arg(node.kwargs, lambda x: env[x])
            env[node] = new_graph.create_node(
                node.op, node.target, args, kwargs, next_node_name(), node.type
            )
        env[node].meta = copy.copy(node.meta)

    new_graph.lint()
    new_gmod = torch.fx.GraphModule(root_gmod, new_graph)
    return new_gmod
