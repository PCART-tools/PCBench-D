def apply_sharding(datapipe, num_of_instances, instance_id):
    graph = torch.utils.data.graph.traverse(datapipe, only_datapipe=True)
    all_pipes = get_all_graph_pipes(graph)
    already_applied_to = None
    for pipe in all_pipes:
        if hasattr(pipe, 'is_shardable'):
            if pipe.is_shardable():
                if hasattr(pipe, 'apply_sharding'):
                    if already_applied_to is not None:
                        raise RuntimeError('This implementation of sharding can be only applied once per instance of DataPipeline.',
                                           'Already applied to', already_applied_to, 'while trying to apply to', pipe)
                    pipe.apply_sharding(num_of_instances, instance_id)
                    already_applied_to = pipe
