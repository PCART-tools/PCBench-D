def apply_shuffle_settings(datapipe, shuffle):
    if shuffle is not None:
        graph = torch.utils.data.graph.traverse(datapipe, only_datapipe=True)
        all_pipes = get_all_graph_pipes(graph)
        for pipe in all_pipes:
            if hasattr(pipe, 'set_shuffle_settings'):
                pipe.set_shuffle_settings(shuffle)
