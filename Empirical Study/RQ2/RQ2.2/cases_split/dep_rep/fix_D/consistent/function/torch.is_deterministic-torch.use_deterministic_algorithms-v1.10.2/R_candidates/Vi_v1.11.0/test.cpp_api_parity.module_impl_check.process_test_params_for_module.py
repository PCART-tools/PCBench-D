def process_test_params_for_module(test_params_dict, device, test_instance_class):
    module_name = compute_module_name(test_params_dict)
    test_params_dict['constructor'] = test_params_dict.get('constructor', getattr(torch.nn, module_name))
    test_instance = test_instance_class(**test_params_dict)
    assert test_instance.get_name().startswith('test_')
    # Example output: `BCELoss_weights_cuda`
    module_variant_name = test_instance.get_name()[5:] + (('_' + device) if device != 'cpu' else '')

    if 'constructor_args' in test_params_dict:
        assert 'cpp_constructor_args' in test_params_dict, (
            "If `constructor_args` is present in test params dict, to enable C++ API parity test, "
            "`cpp_constructor_args` must be present in:\n{}"
            "If you are interested in adding the C++ API parity test, please see:\n"
            "NOTE [How to check NN module / functional API parity between Python and C++ frontends]. \n"
            "If not, please add `test_cpp_api_parity=False` to the test params dict and file an issue about this."
        ).format(pprint.pformat(test_params_dict))

    return TorchNNModuleTestParams(
        module_name=module_name,
        module_variant_name=module_variant_name,
        test_instance=test_instance,
        cpp_constructor_args=test_params_dict.get('cpp_constructor_args', ''),
        arg_dict=compute_arg_dict(test_params_dict, test_instance),
        has_parity=test_params_dict.get('has_parity', True),
        device=device,
        cpp_tmp_folder=tempfile.mkdtemp(),
    )
