def _draw_nets(nets, g):
    nodes = []
    for i, net in enumerate(nets):
        nodes.append(pydot.Node(_escape_label(net)))
        g.add_node(nodes[-1])
        if i > 0:
            g.add_edge(pydot.Edge(nodes[-2], nodes[-1]))
    return nodes
