def test_forward(unit_test_class, test_params):
    functional_variant_name = test_params.functional_variant_name
    cpp_tmp_folder = test_params.cpp_tmp_folder
    # Remove the temporary folder if it exists already
    try_remove_folder(cpp_tmp_folder)
    os.mkdir(cpp_tmp_folder)

    # Run forward on Python functional
    python_output = run_forward(unit_test_class, test_params)

    # Save Python arguments to be used from C++ function
    arg_dict_file_path = compute_temp_file_path(cpp_tmp_folder, functional_variant_name, 'arg_dict')
    serialize_arg_dict_as_script_module(test_params.arg_dict).save(arg_dict_file_path)

    cpp_test_name = '{}_test_forward'.format(test_params.functional_variant_name)
    cpp_test_fn = getattr(unit_test_class.functional_impl_check_cpp_module, cpp_test_name)

    def run_cpp_test_fn_and_check_output():
        forward_output_file_path = compute_temp_file_path(cpp_tmp_folder, functional_variant_name, 'forward_output')

        cpp_test_fn(arg_dict_file_path, forward_output_file_path)
        cpp_output = torch.load(forward_output_file_path)

        # Check that forward outputs are equal
        unit_test_class.assertEqual(
            python_output, cpp_output,
            msg=generate_error_msg("forward output", cpp_output, python_output))

    run_cpp_test_fn_and_check_output()

    # Remove temporary folder that stores C++ outputs
    try_remove_folder(cpp_tmp_folder)
