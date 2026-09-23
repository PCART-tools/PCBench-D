def RunInitNet(model):
    for init_net in model._data_parallel_model_init_nets:
        workspace.RunNetOnce(init_net)
    CreateNet(model)
