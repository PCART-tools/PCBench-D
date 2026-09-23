def get_test_list_by_type(
    run_only: Optional[List[str]], test_type: TestType
) -> TestList:
    test_list: TestList = []
    binary_folder = get_oss_binary_folder(test_type)
    g = os.walk(binary_folder)
    for _, _, file_list in g:
        for file_name in file_list:
            if run_only is not None and file_name not in run_only:
                continue
            # target pattern in oss is used in printing report -- which tests we have run
            test: Test = Test(
                name=file_name,
                target_pattern=file_name,
                test_set="",
                test_type=test_type,
            )
            test_list.append(test)
    return test_list
