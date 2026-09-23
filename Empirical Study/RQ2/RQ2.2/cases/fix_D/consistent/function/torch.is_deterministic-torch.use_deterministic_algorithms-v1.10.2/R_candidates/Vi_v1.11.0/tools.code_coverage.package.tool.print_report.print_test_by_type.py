def print_test_by_type(
    tests: TestList, test_set_by_type: Set[str], type_name: str, summary_file: IO[str]
) -> None:

    print("Tests " + type_name + " to collect coverage:", file=summary_file)
    for test in tests:
        if is_this_type_of_tests(test.name, test_set_by_type):
            print(test.target_pattern, file=summary_file)
    print(file=summary_file)
