def AddParameterUpdate(model):
    """ Simple plain SGD update -- not tuned to actually train the models """
    ITER = brew.iter(model, "iter")
    LR = model.net.LearningRate(
        ITER, "LR", base_lr=-1e-8, policy="step", stepsize=10000, gamma=0.999)
    ONE = model.param_init_net.ConstantFill([], "ONE", shape=[1], value=1.0)
    for param in model.params:
        param_grad = model.param_to_grad[param]
        model.net.WeightedSum([param, ONE, param_grad, LR], param)
