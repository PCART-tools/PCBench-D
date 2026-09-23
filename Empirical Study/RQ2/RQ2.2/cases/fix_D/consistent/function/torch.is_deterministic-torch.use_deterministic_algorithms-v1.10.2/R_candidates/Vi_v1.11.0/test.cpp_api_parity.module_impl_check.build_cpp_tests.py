def build_cpp_tests(unit_test_class, print_cpp_source=False):
    assert len(unit_test_class.module_test_params_map) > 0
    cpp_sources = TORCH_NN_COMMON_TEST_HARNESS + SAMPLE_MODULE_CPP_SOURCE
    functions = []
    for test_name, test_params in unit_test_class.module_test_params_map.items():
        cpp_sources += generate_test_cpp_sources(
            test_params=test_params, template=TORCH_NN_MODULE_TEST_FORWARD_BACKWARD)
        functions.append('{}_test_forward_backward'.format(test_params.module_variant_name))
    if print_cpp_source:
        print(cpp_sources)

    cpp_module = compile_cpp_code_inline(
        name='module_impl_check',
        cpp_sources=cpp_sources,
        functions=functions)
    unit_test_class.module_impl_check_cpp_module = cpp_module
