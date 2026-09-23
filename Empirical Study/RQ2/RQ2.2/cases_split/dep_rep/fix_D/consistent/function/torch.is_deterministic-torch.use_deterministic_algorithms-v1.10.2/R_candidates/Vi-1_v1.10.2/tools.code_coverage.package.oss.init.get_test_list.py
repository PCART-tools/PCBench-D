def get_test_list(run_only: Optional[List[str]]) -> TestList:
    test_list: TestList = []
    # add c++ test list
    test_list.extend(get_test_list_by_type(run_only, TestType.CPP))
    # add python test list
    py_run_only = get_python_run_only(run_only)
    test_list.extend(get_test_list_by_type(py_run_only, TestType.PY))

    # not find any test to run
    if not test_list:
        raise_no_test_found_exception(
            get_oss_binary_folder(TestType.CPP), get_oss_binary_folder(TestType.PY)
        )
    return test_list
