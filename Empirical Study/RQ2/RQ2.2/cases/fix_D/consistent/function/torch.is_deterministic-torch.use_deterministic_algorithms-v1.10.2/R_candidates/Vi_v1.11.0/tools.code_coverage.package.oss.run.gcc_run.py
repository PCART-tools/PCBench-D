def gcc_run(tests: TestList) -> None:
    start_time = time.time()
    for test in tests:
        # binary file
        binary_file = get_oss_binary_file(test.name, test.test_type)
        gcc_coverage.run_target(binary_file, test.test_type)
    print_time("run binaries takes time: ", start_time, summary_time=True)
