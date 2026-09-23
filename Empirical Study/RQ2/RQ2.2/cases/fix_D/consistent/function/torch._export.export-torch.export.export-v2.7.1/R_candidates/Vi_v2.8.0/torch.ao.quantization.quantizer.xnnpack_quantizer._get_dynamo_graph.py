def _get_dynamo_graph(function: Callable, inputs) -> torch.fx.Graph:
    gm, _ = torchdynamo.export(function, aten_graph=True)(*inputs)
    gm.graph.eliminate_dead_code()
    return gm.graph
