def get_test_case_args(test_module, using_pytest) -> List[str]:
    args = []
    # if test_module not specified or specified with '__all__' then run all tests
    if (
        test_module not in SPECIFIED_TEST_CASES_DICT
        or "__all__" in SPECIFIED_TEST_CASES_DICT[test_module]
    ):
        return args

    if using_pytest:
        args.append("-k")
        args.append(" or ".join(SPECIFIED_TEST_CASES_DICT[test_module]))
    else:
        for test in SPECIFIED_TEST_CASES_DICT[test_module]:
            args.append("-k")
            args.append(test)

    return args
