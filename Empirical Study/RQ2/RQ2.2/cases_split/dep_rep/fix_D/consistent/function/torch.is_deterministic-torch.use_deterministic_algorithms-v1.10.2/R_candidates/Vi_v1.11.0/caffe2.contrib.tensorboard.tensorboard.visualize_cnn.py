def visualize_cnn(cnn, **kwargs):
    g = tb_exporter.cnn_to_graph_def(cnn, **kwargs)
    _show_graph(g)
