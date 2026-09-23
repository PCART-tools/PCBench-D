def is_torch_nn_functional_test(test_params_dict):
    return 'wrap_functional' in str(test_params_dict.get('constructor', ''))
