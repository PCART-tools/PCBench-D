def compute_arg_dict(test_params_dict, test_instance):
    arg_dict = {
        'input': [],
        'target': [],
        'extra_args': [],
        'other': [],
    }

    def put_args_into_arg_dict(arg_type, arg_type_prefix, args):
        for i, arg in enumerate(args):
            arg_dict[arg_type].append(CppArg(name=arg_type_prefix + str(i), value=arg))

    put_args_into_arg_dict('input', 'i', convert_to_list(test_instance._get_input()))
    if is_criterion_test(test_instance):
        put_args_into_arg_dict('target', 't', convert_to_list(test_instance._get_target()))
    if test_instance.extra_args:
        put_args_into_arg_dict('extra_args', 'e', convert_to_list(test_instance.extra_args))

    cpp_var_map = test_params_dict.get('cpp_var_map', {})
    for arg_name, arg_value in cpp_var_map.items():
        if isinstance(arg_value, str):
            if arg_value == '_get_input()':
                arg_dict['other'].append(CppArg(name=arg_name, value=test_instance._get_input()))
            else:
                raise RuntimeError("`{}` has unsupported string value: {}".format(arg_name, arg_value))
        elif isinstance(arg_value, torch.Tensor):
            arg_dict['other'].append(CppArg(name=arg_name, value=arg_value))
        else:
            raise RuntimeError("`{}` has unsupported value: {}".format(arg_name, arg_value))

    return arg_dict
