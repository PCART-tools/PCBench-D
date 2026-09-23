def CreateNet(model, overwrite=False):
    for net_iters in model._data_parallel_model_nets:
        if isinstance(net_iters, tuple):
            workspace.CreateNet(net_iters[0], overwrite=overwrite)
        else:
            workspace.CreateNet(net_iters, overwrite=overwrite)
