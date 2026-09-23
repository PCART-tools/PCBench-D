def get_expected_file(function_ptr):
    module_id = function_ptr.__class__.__module__
    test_file = sys.modules[module_id].__file__
    # Look for the .py file (since __file__ could be pyc).
    test_file = ".".join(test_file.split('.')[:-1]) + '.py'

    # Use realpath to follow symlinks appropriately.
    test_dir = os.path.dirname(os.path.realpath(test_file))
    functionName = function_ptr.id().split('.')[-1]
    return os.path.join(test_dir,
                        "expect",
                        'TestTensorBoard.' + functionName + ".expect")
