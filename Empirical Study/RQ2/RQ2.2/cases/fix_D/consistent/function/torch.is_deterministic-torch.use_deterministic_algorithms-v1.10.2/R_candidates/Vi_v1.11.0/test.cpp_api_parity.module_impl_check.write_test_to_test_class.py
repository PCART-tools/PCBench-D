def write_test_to_test_class(
        unit_test_class, test_params_dict, test_instance_class, parity_table, devices):
    assert not is_torch_nn_functional_test(test_params_dict)

    module_name = compute_module_name(test_params_dict)

    assert hasattr(torch.nn, module_name), (
        "`torch.nn` doesn't have module `{}`. "
        "If you are adding a new test, please set `fullname` using format `ModuleName_desc` "
        "or set `module_name` using format `ModuleName` in the module test dict:\n{}"
    ).format(module_name, pprint.pformat(test_params_dict))

    module_full_name = 'torch::nn::' + module_name

    assert module_full_name in parity_table['torch::nn'], (
        "Please add `{}` entry to `torch::nn` section of `test/cpp_api_parity/parity-tracker.md`. "
        "(Discovered while processing\n{}.)").format(module_full_name, pprint.pformat(test_params_dict))

    for device in devices:
        test_params = process_test_params_for_module(
            test_params_dict=test_params_dict,
            device=device,
            test_instance_class=test_instance_class,
        )
        try_remove_folder(test_params.cpp_tmp_folder)
        unit_test_name = 'test_torch_nn_{}'.format(test_params.module_variant_name)
        unit_test_class.module_test_params_map[unit_test_name] = test_params

        def test_fn(self):
            test_forward_backward(
                unit_test_class=self, test_params=unit_test_class.module_test_params_map[self._testMethodName])

        test_fn = decorate_test_fn(
            test_fn=test_fn,
            test_cuda=test_params_dict.get('test_cuda', True),
            has_impl_parity=parity_table['torch::nn'][module_full_name][0] and
            test_params_dict.get('has_parity', True),
            device=device)

        add_test(unit_test_class, unit_test_name, test_fn)
