def test_forward_backward(unit_test_class, test_params):
    module_variant_name = test_params.module_variant_name
    cpp_tmp_folder = test_params.cpp_tmp_folder
    # Remove the temporary folder if it exists already
    try_remove_folder(cpp_tmp_folder)
    os.mkdir(cpp_tmp_folder)

    # Run forward and backward on Python module
    script_module, python_output, python_grad_dict = run_python_forward_backward(unit_test_class, test_params)

    # Save Python module and arguments to be used from C++ function
    module_file_path = compute_temp_file_path(cpp_tmp_folder, module_variant_name, 'module')
    arg_dict_file_path = compute_temp_file_path(cpp_tmp_folder, module_variant_name, 'arg_dict')
    script_module.save(module_file_path)
    serialize_arg_dict_as_script_module(test_params.arg_dict).save(arg_dict_file_path)

    cpp_test_name = '{}_test_forward_backward'.format(test_params.module_variant_name)
    cpp_test_fn = getattr(unit_test_class.module_impl_check_cpp_module, cpp_test_name)

    def run_cpp_test_fn_and_check_output():
        forward_output_file_path = compute_temp_file_path(cpp_tmp_folder, module_variant_name, 'forward_output')
        backward_grad_dict_file_path = compute_temp_file_path(cpp_tmp_folder, module_variant_name, 'backward_grad_dict')

        cpp_test_fn(arg_dict_file_path, module_file_path, forward_output_file_path, backward_grad_dict_file_path)
        cpp_output = torch.load(forward_output_file_path)
        cpp_grad_dict = torch.load(backward_grad_dict_file_path)

        # Check that forward outputs are equal
        unit_test_class.assertEqual(python_output, cpp_output,
                                    msg=generate_error_msg("forward output", cpp_output, python_output))

        # Check that module parameter gradients are equal after backward pass
        unit_test_class.assertEqual(
            len(python_grad_dict), len(cpp_grad_dict),
            msg=generate_error_msg("# of parameters", len(cpp_grad_dict), len(python_grad_dict)))
        for key in python_grad_dict:
            param_name = None
            for suffix in ['_grad', '_grad_indices', '_grad_values']:
                if key.endswith(suffix):
                    param_name = key[:-len(suffix)]
                    break
            assert param_name is not None
            sparsity_str = 'sparse' if key.endswith('_grad_indices') or key.endswith('_grad_values') else 'dense'

            unit_test_class.assertTrue(
                key in cpp_grad_dict,
                msg=generate_error_msg(
                    "\"Does module have a parameter named `{}` with {} gradient?\"".format(param_name, sparsity_str),
                    False, True))
            unit_test_class.assertEqual(
                python_grad_dict[key], cpp_grad_dict[key],
                msg=generate_error_msg(
                    "`{}`'s {} gradient (`{}`)".format(param_name, sparsity_str, key),
                    cpp_grad_dict[key], python_grad_dict[key]))

    run_cpp_test_fn_and_check_output()

    # Remove temporary folder that stores C++ outputs
    try_remove_folder(cpp_tmp_folder)
