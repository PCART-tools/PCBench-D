def RunNet(model, num_iterations):
    for net_iter in model._data_parallel_model_nets:
        if isinstance(net_iter, tuple):
            workspace.RunNet(net_iter[0].Proto().name, net_iter[1])
        else:
            workspace.RunNet(net_iter, num_iterations)
