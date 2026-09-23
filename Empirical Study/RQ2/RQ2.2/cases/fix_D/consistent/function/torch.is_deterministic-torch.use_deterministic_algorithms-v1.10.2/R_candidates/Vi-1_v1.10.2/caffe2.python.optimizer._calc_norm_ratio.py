def _calc_norm_ratio(model, params, name_scope, param_to_device, max_gradient_norm):
    with core.NameScope(name_scope):
        grad_squared_sums = []
        for i, param in enumerate(params):
            device = get_param_device(str(param.blob), param.grad, param_to_device)

            with core.DeviceScope(device):
                grad = (
                    param.grad
                    if not isinstance(param.grad, core.GradientSlice)
                    else param.grad.values
                )

                grad_squared_sum_name = "grad_{}_squared_sum".format(i)
                grad_squared_sum = model.net.SumSqrElements(grad, grad_squared_sum_name)
                grad_squared_sum_cpu = model.net.EnsureCPUOutput(grad_squared_sum)
                grad_squared_sums.append(grad_squared_sum_cpu)

        with core.DeviceScope(core.DeviceOption(caffe2_pb2.CPU)):
            grad_squared_full_sum = model.net.Sum(
                grad_squared_sums, "grad_squared_full_sum"
            )
            global_norm = model.net.Pow(
                grad_squared_full_sum, "global_norm", exponent=0.5
            )
            clip_norm = model.param_init_net.ConstantFill(
                [], "clip_norm", shape=[], value=float(max_gradient_norm)
            )
            max_norm = model.net.Max([global_norm, clip_norm], "max_norm")
            norm_ratio = model.net.Div([clip_norm, max_norm], "norm_ratio")
            return norm_ratio
