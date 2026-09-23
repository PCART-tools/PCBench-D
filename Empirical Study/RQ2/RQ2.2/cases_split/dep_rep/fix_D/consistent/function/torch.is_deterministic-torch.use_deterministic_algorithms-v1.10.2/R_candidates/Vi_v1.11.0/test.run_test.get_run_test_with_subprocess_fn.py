def get_run_test_with_subprocess_fn():
    return lambda test_module, test_directory, options: run_test_with_subprocess(test_module, test_directory, options)
