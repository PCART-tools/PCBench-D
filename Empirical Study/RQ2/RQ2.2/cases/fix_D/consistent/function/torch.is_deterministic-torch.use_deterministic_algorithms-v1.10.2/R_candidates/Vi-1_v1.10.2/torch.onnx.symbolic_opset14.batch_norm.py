@parse_args("v", "v", "v", "v", "v", "i", "f", "f", "i")
def batch_norm(g, input, weight, bias, running_mean, running_var, training, momentum, eps, cudnn_enabled):
    sym_help.check_training_mode(training, "batch_norm")
    weight, bias, running_mean, running_var = sym_help._batchnorm_helper(g, input, weight, bias, running_mean, running_var)
    out = g.op("BatchNormalization", input, weight, bias, running_mean, running_var,
               epsilon_f=eps,
               momentum_f=1 - momentum,
               training_mode_i=0 if not training else 1,
               outputs=1 if not training else 3)
    if not training:
        return out
    else:
        res, new_running_mean, new_running_var = out
        new_running_mean.setType(running_mean.type())
        new_running_var.setType(running_var.type())
        return res
