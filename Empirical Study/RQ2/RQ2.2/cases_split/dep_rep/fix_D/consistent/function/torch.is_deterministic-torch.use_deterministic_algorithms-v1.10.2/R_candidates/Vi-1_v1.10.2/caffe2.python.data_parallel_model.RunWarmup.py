def RunWarmup(model):
    workspace.RunNet(model.net, model._warmup_iterations)
    workspace.RunNetOnce(model._warmup_broadcast)
