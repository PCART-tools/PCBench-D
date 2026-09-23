def get_selected_tests(options):
    # First make sure run specific test cases options are processed.
    if options.run_specified_test_cases:
        if options.use_specified_test_cases_by == "include":
            options.include = list(SPECIFIED_TEST_CASES_DICT.keys())
        elif options.use_specified_test_cases_by == "bring-to-front":
            options.bring_to_front = list(SPECIFIED_TEST_CASES_DICT.keys())

    selected_tests = options.include

    # filter if there's JIT only and distributed only test options
    if options.jit:
        selected_tests = list(
            filter(lambda test_name: "jit" in test_name, selected_tests)
        )

    if options.distributed_tests:
        selected_tests = list(
            filter(lambda test_name: test_name in DISTRIBUTED_TESTS, selected_tests)
        )

    # Only run fx2trt test with specified option argument
    if options.fx2trt_tests:
        selected_tests = list(
            filter(lambda test_name: test_name in FX2TRT_TESTS, selected_tests)
        )
    else:
        options.exclude.extend(FX2TRT_TESTS)

    # Filter to only run core tests when --core option is specified
    if options.core:
        selected_tests = list(
            filter(lambda test_name: test_name in CORE_TEST_LIST, selected_tests)
        )

    # process reordering
    if options.bring_to_front:
        to_front = set(options.bring_to_front)
        selected_tests = options.bring_to_front + list(
            filter(lambda name: name not in to_front, selected_tests)
        )

    if options.first:
        first_index = find_test_index(options.first, selected_tests)
        selected_tests = selected_tests[first_index:]

    if options.last:
        last_index = find_test_index(options.last, selected_tests, find_last_index=True)
        selected_tests = selected_tests[: last_index + 1]

    # process exclusion
    if options.exclude_jit_executor:
        options.exclude.extend(JIT_EXECUTOR_TESTS)

    if options.exclude_distributed_tests:
        options.exclude.extend(DISTRIBUTED_TESTS)

    if options.exclude_fx2trt_tests:
        options.exclude.extend(FX2TRT_TESTS)

    selected_tests = exclude_tests(options.exclude, selected_tests)

    if sys.platform == "win32" and not options.ignore_win_blocklist:
        target_arch = os.environ.get("VSCMD_ARG_TGT_ARCH")
        if target_arch != "x64":
            WINDOWS_BLOCKLIST.append("cpp_extensions_aot_no_ninja")
            WINDOWS_BLOCKLIST.append("cpp_extensions_aot_ninja")
            WINDOWS_BLOCKLIST.append("cpp_extensions_jit")
            WINDOWS_BLOCKLIST.append("jit")
            WINDOWS_BLOCKLIST.append("jit_fuser")

        # This is exception that's caused by this issue https://github.com/pytorch/pytorch/issues/69460
        # This below code should be removed once this issue is solved
        if torch.version.cuda is not None and LooseVersion(torch.version.cuda) >= "11.5":
            WINDOWS_BLOCKLIST.append("test_cpp_extensions_aot")
            WINDOWS_BLOCKLIST.append("test_cpp_extensions_aot_ninja")
            WINDOWS_BLOCKLIST.append("test_cpp_extensions_aot_no_ninja")

        selected_tests = exclude_tests(WINDOWS_BLOCKLIST, selected_tests, "on Windows")

    elif TEST_WITH_ROCM:
        selected_tests = exclude_tests(ROCM_BLOCKLIST, selected_tests, "on ROCm")

    # sharding
    if options.shard:
        assert len(options.shard) == 2, "Unexpected shard format"
        assert min(options.shard) > 0, "Shards must be positive numbers"
        which_shard, num_shards = options.shard
        assert (
            which_shard <= num_shards
        ), "Selected shard must be less than or equal to total number of shards"
        assert num_shards <= len(
            selected_tests
        ), f"Number of shards must be less than {len(selected_tests)}"
        # TODO: fix this to use test_times_filename, but currently this is not working
        # because setting the export arg immeidately halts the test execution.
        selected_tests = get_shard_based_on_S3(
            which_shard, num_shards, selected_tests, TEST_TIMES_FILE
        )

    # skip all distributed tests if distributed package is not available.
    if not dist.is_available():
        selected_tests = exclude_tests(DISTRIBUTED_TESTS, selected_tests,
                                       "PyTorch is built without distributed support.")

    return selected_tests
