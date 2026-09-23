def add_quantization_param_args_(op, q_param):
    op.arg.extend(
        [
            utils.MakeArgument("Y_scale", q_param.scale),
            utils.MakeArgument("Y_zero_point", q_param.zero_point),
        ]
    )
