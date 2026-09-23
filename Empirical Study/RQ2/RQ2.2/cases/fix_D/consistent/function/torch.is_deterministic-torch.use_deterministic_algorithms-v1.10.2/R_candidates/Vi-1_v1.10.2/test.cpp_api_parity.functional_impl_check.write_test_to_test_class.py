def write_test_to_test_class(
        unit_test_class, test_params_dict, test_instance_class, parity_table, devices):
    assert is_torch_nn_functional_test(test_params_dict)

    assert 'cpp_options_args' in test_params_dict or 'cpp_function_call' in test_params_dict, (
        "To enable C++ API parity test, "
        "`cpp_options_args` or `cpp_function_call` entry must be present in test params dict:\n{}. \n"
        "If you are interested in adding the C++ API parity test, please see:\n"
        "NOTE [How to check NN module / functional API parity between Python and C++ frontends]. \n"
        "If not, please add `test_cpp_api_parity=False` to the test params dict and file an issue about this."
    ).format(pprint.pformat(test_params_dict))

    assert not ('cpp_options_args' in test_params_dict and 'cpp_function_call' in test_params_dict), (
        "Only one of `cpp_options_args` and `cpp_function_call` entries "
        "should be present in test params dict:\n{}").format(pprint.pformat(test_params_dict))

    functional_name = compute_functional_name(test_params_dict)

    assert hasattr(torch.nn.functional, functional_name), \
        "`torch.nn.functional` doesn't have function `{}`. (Discovered while processing\n{}.)".format(
            functional_name, pprint.pformat(test_params_dict))

    functional_full_name = 'F::' + functional_name

    assert functional_full_name in parity_table['torch::nn::functional'], (
        "Please add `{}` entry to `torch::nn::functional` section of `test/cpp_api_parity/parity-tracker.md`. "
        "(Discovered while processing\n{}.)").format(functional_full_name, pprint.pformat(test_params_dict))

    for device in devices:
        test_params = process_test_params_for_functional(
            test_params_dict=test_params_dict,
            device=device,
            test_instance_class=test_instance_class,
        )
        try_remove_folder(test_params.cpp_tmp_folder)
        unit_test_name = 'test_torch_nn_functional_{}'.format(test_params.functional_variant_name)
        unit_test_class.functional_test_params_map[unit_test_name] = test_params

        def test_fn(self):
            test_forward(
                unit_test_class=self, test_params=unit_test_class.functional_test_params_map[self._testMethodName])

        test_fn = decorate_test_fn(
            test_fn=test_fn,
            test_cuda=test_params_dict.get('test_cuda', True),
            has_impl_parity=parity_table['torch::nn::functional'][functional_full_name][0] and
            test_params_dict.get('has_parity', True),
            device=device)

        add_test(unit_test_class, unit_test_name, test_fn)
