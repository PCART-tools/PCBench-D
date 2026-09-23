def visualize_net(nets, **kwargs):
    g = tb_exporter.nets_to_graph_def(nets, **kwargs)
    _show_graph(g)
