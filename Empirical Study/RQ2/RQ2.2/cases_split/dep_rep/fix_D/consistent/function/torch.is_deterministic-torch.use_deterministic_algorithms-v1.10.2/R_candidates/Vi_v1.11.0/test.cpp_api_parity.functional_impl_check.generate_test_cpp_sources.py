def generate_test_cpp_sources(test_params, template):
    cpp_args_construction_stmts, _ = compute_cpp_args_construction_stmts_and_forward_arg_symbols(test_params)

    test_cpp_sources = template.substitute(
        functional_variant_name=test_params.functional_variant_name,
        cpp_args_construction_stmts=";\n  ".join(cpp_args_construction_stmts),
        cpp_function_call=test_params.cpp_function_call,
    )
    return test_cpp_sources
