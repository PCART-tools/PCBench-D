def compute_cpp_args_construction_stmts_and_forward_arg_symbols(test_params):
    device = test_params.device
    cpp_forward_args_symbols = []

    def add_cpp_forward_args(args):
        args_stmts = []
        for arg_name, _ in args:
            args_stmts.append('auto {} = arg_dict.at("{}")'.format(arg_name, arg_name))
            cpp_forward_args_symbols.append(arg_name)
        return args_stmts

    cpp_forward_input_args_stmts = set_cpp_tensors_requires_grad(move_cpp_tensors_to_device(
        add_cpp_forward_args(test_params.arg_dict['input']), device), test_params.arg_dict['input'])
    cpp_forward_target_args_stmts = move_cpp_tensors_to_device(
        add_cpp_forward_args(test_params.arg_dict['target']), device)
    cpp_forward_extra_args_stmts = move_cpp_tensors_to_device(
        add_cpp_forward_args(test_params.arg_dict['extra_args']), device)

    # Build the list of other arguments needed
    cpp_other_args_stmts = []
    for arg_name, _ in test_params.arg_dict['other']:
        cpp_other_args_stmts.append('auto {} = arg_dict.at("{}")'.format(arg_name, arg_name))
    cpp_other_args_stmts = move_cpp_tensors_to_device(cpp_other_args_stmts, device)

    cpp_args_construction_stmts = cpp_forward_input_args_stmts + cpp_forward_target_args_stmts + \
        cpp_forward_extra_args_stmts + cpp_other_args_stmts

    return cpp_args_construction_stmts, cpp_forward_args_symbols
