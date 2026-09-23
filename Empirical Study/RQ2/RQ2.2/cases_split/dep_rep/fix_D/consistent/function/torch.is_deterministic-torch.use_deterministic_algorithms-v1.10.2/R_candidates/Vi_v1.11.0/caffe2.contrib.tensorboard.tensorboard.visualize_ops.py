def visualize_ops(ops, **kwargs):
    g = tb_exporter.ops_to_graph_def(ops, **kwargs)
    _show_graph(g)
