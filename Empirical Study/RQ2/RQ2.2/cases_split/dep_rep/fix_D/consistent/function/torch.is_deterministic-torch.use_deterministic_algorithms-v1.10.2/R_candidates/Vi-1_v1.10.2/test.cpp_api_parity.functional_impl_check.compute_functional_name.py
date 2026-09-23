def compute_functional_name(test_params_dict):
    def camel_case_to_snake_case(camel_case_str):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_case_str).lower()

    if 'cpp_options_args' in test_params_dict:
        # Expected format for `cpp_options_args`: `F::FunctionalFuncOptions(...)`
        # Example output: `binary_cross_entropy`
        return camel_case_to_snake_case(
            test_params_dict['cpp_options_args'].split('(')[0].replace('F::', '').replace('FuncOptions', ''))
    elif 'cpp_function_call' in test_params_dict:
        # Expected format for `cpp_function_call`: `F::functional_name(...)`
        # Example output: `binary_cross_entropy`
        return test_params_dict['cpp_function_call'].split('(')[0].replace('F::', '')
    else:
        raise RuntimeError(
            "`cpp_options_args` or `cpp_function_call` entry must be present in test params dict:\n{}".format(
                pprint.pformat(test_params_dict)))
