def build_conv_model(model_name, batch_size):
    model_gen_map = conv_model_generators()
    assert model_name in model_gen_map, "Model " + model_name + " not found"
    model, input_size = model_gen_map[model_name]("NCHW", None)

    input_shape = [batch_size, 3, input_size, input_size]
    if model_name == "MLP":
        input_shape = [batch_size, input_size]

    model.param_init_net.GaussianFill(
        [],
        "data",
        shape=input_shape,
        mean=0.0,
        std=1.0
    )
    model.param_init_net.UniformIntFill(
        [],
        "label",
        shape=[batch_size, ],
        min=0,
        max=999
    )

    model.AddGradientOperators(["loss"])

    ITER = brew.iter(model, "iter")
    LR = model.net.LearningRate(
        ITER, "LR", base_lr=-1e-8, policy="step", stepsize=10000, gamma=0.999)
    ONE = model.param_init_net.ConstantFill([], "ONE", shape=[1], value=1.0)
    for param in model.params:
        param_grad = model.param_to_grad[param]
        model.net.WeightedSum([param, ONE, param_grad, LR], param)

    return model
