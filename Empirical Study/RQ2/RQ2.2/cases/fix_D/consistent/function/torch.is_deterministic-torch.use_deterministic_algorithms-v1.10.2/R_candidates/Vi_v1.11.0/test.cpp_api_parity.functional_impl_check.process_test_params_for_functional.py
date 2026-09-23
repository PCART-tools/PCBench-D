def process_test_params_for_functional(test_params_dict, device, test_instance_class):
    test_instance = test_instance_class(**test_params_dict)
    functional_name = compute_functional_name(test_params_dict)
    assert test_instance.get_name().startswith('test_')
    # Example output: `BCELoss_no_reduce_cuda`
    functional_variant_name = test_instance.get_name()[5:] + (('_' + device) if device != 'cpu' else '')
    arg_dict = compute_arg_dict(test_params_dict, test_instance)

    return TorchNNFunctionalTestParams(
        functional_name=functional_name,
        functional_variant_name=functional_variant_name,
        test_instance=test_instance,
        cpp_function_call=compute_cpp_function_call(test_params_dict, arg_dict, functional_name),
        arg_dict=arg_dict,
        has_parity=test_params_dict.get('has_parity', True),
        device=device,
        cpp_tmp_folder=tempfile.mkdtemp(),
    )
