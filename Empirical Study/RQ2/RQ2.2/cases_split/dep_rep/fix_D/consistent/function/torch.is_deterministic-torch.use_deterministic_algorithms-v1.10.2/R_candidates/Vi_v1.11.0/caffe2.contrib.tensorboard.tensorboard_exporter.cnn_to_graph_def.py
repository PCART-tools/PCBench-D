def cnn_to_graph_def(cnn, **kwargs):
    return nets_to_graph_def([cnn.param_init_net, cnn.net], **kwargs)
