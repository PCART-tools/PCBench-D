def check_test_defined_in_running_script(test_case):
    if running_script_path is None:
        return
    test_case_class_file = os.path.abspath(os.path.realpath(inspect.getfile(test_case.__class__)))
    assert test_case_class_file == running_script_path, "Class of loaded TestCase \"{}\" " \
        "is not defined in the running script \"{}\", but in \"{}\". Did you " \
        "accidentally import a unittest.TestCase from another file?".format(
            test_case.id(), running_script_path, test_case_class_file)
