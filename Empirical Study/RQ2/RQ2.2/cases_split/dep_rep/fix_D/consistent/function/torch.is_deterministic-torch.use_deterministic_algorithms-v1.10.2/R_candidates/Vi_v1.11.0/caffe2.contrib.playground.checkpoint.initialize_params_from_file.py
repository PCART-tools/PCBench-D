def initialize_params_from_file(
        model, weights_file, num_xpus, opts,
        broadcast_computed_param=False, reset_epoch=False):
    start_epoch, lr, best_metric = initialize_master_xpu_model_params(
        model, weights_file, opts, reset_epoch)
    broadcast_parameters(opts, model, num_xpus, broadcast_computed_param)
    return start_epoch, lr, best_metric
