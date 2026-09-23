def run_target(binary_file: str, test_type: TestType) -> None:
    print_log("start run", test_type.value, "test: ", binary_file)
    start_time = time.time()
    assert test_type in {TestType.CPP, TestType.PY}
    if test_type == TestType.CPP:
        run_cpp_test(binary_file)
    else:
        run_oss_python_test(binary_file)

    print_time(" time: ", start_time)
