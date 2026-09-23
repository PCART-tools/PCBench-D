def compute_cpp_function_call(test_params_dict, arg_dict, functional_name):
    if 'cpp_function_call' in test_params_dict:
        return test_params_dict['cpp_function_call']
    elif 'cpp_options_args' in test_params_dict:
        cpp_forward_args_symbols = [arg_name for arg_name, _ in
                                    arg_dict['input'] + arg_dict['target'] + arg_dict['extra_args']]
        return 'F::{}({}, {})'.format(
            functional_name, ", ".join(cpp_forward_args_symbols), test_params_dict['cpp_options_args'])
    else:
        raise RuntimeError(
            "`cpp_options_args` or `cpp_function_call` entry must be present in test params dict:\n{}".format(
                pprint.pformat(test_params_dict)))
