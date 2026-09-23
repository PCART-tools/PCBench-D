def removeExceptions(graph):
    for n in graph.findAllNodes('prim::RaiseException'):
        n.destroy()
