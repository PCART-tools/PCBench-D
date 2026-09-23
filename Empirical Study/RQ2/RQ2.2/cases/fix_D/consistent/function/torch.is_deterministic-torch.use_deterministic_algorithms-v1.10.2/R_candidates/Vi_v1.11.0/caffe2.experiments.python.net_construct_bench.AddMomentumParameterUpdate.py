def AddMomentumParameterUpdate(train_model, LR):
    '''
    Add the momentum-SGD update.
    '''
    params = train_model.GetParams()
    assert(len(params) > 0)
    ONE = train_model.param_init_net.ConstantFill(
        [], "ONE", shape=[1], value=1.0,
    )
    NEGONE = train_model.param_init_net.ConstantFill(
        [], 'NEGONE', shape=[1], value=-1.0,
    )

    for param in params:
        param_grad = train_model.param_to_grad[param]
        param_momentum = train_model.param_init_net.ConstantFill(
            [param], param + '_momentum', value=0.0
        )

        # Update param_grad and param_momentum in place
        train_model.net.MomentumSGD(
            [param_grad, param_momentum, LR],
            [param_grad, param_momentum],
            momentum=0.9,
            nesterov=1
        )

        # Update parameters by applying the moment-adjusted gradient
        train_model.WeightedSum(
            [param, ONE, param_grad, NEGONE],
            param
        )
