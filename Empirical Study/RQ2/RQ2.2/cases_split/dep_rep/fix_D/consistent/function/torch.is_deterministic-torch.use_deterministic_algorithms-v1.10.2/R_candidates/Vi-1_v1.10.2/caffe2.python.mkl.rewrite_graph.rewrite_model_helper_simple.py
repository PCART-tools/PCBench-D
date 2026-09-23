def rewrite_model_helper_simple(model):
    model = copy.deepcopy(model)
    # All parameter initialization should run on MKL
    rewrite_init_net_simple(model.param_init_net.Proto())
    rewrite_run_net_simple(model.net.Proto())
    return model
