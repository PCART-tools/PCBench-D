def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the PyTorch unit test suite",
        epilog="where TESTS is any of: {}".format(", ".join(TESTS)),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="print verbose information and test-by-test results",
    )
    parser.add_argument("--jit", "--jit", action="store_true", help="run all jit tests")
    parser.add_argument(
        "--distributed-tests",
        "--distributed-tests",
        action="store_true",
        help="run all distributed tests",
    )
    parser.add_argument(
        "--fx2trt-tests",
        "--fx2trt-tests",
        action="store_true",
        help="run all fx2trt tests",
    )
    parser.add_argument(
        "-core",
        "--core",
        action="store_true",
        help="Only run core tests, or tests that validate PyTorch's ops, modules,"
        "and autograd. They are defined by CORE_TEST_LIST."
    )
    parser.add_argument(
        "-pt",
        "--pytest",
        action="store_true",
        help="If true, use `pytest` to execute the tests. E.g., this runs "
        "TestTorch with pytest in verbose and coverage mode: "
        "python run_test.py -vci torch -pt",
    )
    parser.add_argument(
        "-c",
        "--coverage",
        action="store_true",
        help="enable coverage",
        default=PYTORCH_COLLECT_COVERAGE,
    )
    parser.add_argument(
        "-i",
        "--include",
        nargs="+",
        choices=TestChoices(TESTS),
        default=TESTS,
        metavar="TESTS",
        help="select a set of tests to include (defaults to ALL tests)."
        " tests must be a part of the TESTS list defined in run_test.py",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        nargs="+",
        choices=TESTS,
        metavar="TESTS",
        default=[],
        help="select a set of tests to exclude",
    )
    parser.add_argument(
        "-f",
        "--first",
        choices=TESTS,
        metavar="TESTS",
        help="select the test to start from (excludes previous tests)",
    )
    parser.add_argument(
        "-l",
        "--last",
        choices=TESTS,
        metavar="TESTS",
        help="select the last test to run (excludes following tests)",
    )
    parser.add_argument(
        "--bring-to-front",
        nargs="+",
        choices=TestChoices(TESTS),
        default=[],
        metavar="TESTS",
        help="select a set of tests to run first. This can be used in situations"
        " where you want to run all tests, but care more about some set, "
        "e.g. after making a change to a specific component",
    )
    parser.add_argument(
        "--ignore-win-blocklist",
        action="store_true",
        help="always run blocklisted windows tests",
    )
    # NS: Disable target determination until it can be made more reliable
    # parser.add_argument(
    #     "--determine-from",
    #     help="File of affected source filenames to determine which tests to run.",
    # )
    parser.add_argument(
        "--continue-through-error",
        action="store_true",
        help="Runs the full test suite despite one of the tests failing",
        default=strtobool(os.environ.get("CONTINUE_THROUGH_ERROR", "False")),
    )
    parser.add_argument(
        "additional_unittest_args",
        nargs="*",
        help="additional arguments passed through to unittest, e.g., "
        "python run_test.py -i sparse -- TestSparse.test_factory_size_check",
    )
    parser.add_argument(
        "--export-past-test-times",
        nargs="?",
        type=str,
        const=TEST_TIMES_FILE,
        help="dumps test times from previous S3 stats into a file, format JSON",
    )
    parser.add_argument(
        "--shard",
        nargs=2,
        type=int,
        help="runs a shard of the tests (taking into account other selections), e.g., "
        "--shard 2 3 will break up the selected tests into 3 shards and run the tests "
        "in the 2nd shard (the first number should not exceed the second)",
    )
    parser.add_argument(
        "--exclude-jit-executor",
        action="store_true",
        help="exclude tests that are run for a specific jit config",
    )
    parser.add_argument(
        "--exclude-distributed-tests",
        action="store_true",
        help="exclude distributed tests",
    )
    parser.add_argument(
        "--exclude-fx2trt-tests",
        action="store_true",
        help="exclude fx2trt tests",
    )
    parser.add_argument(
        "--run-specified-test-cases",
        nargs="?",
        type=str,
        const=SPECIFIED_TEST_CASES_FILE,
        help="load specified test cases file dumped from previous OSS CI stats, format CSV. "
        " If all test cases should run for a <test_module> please add a single row: \n"
        " test_filename,test_case_name\n"
        " ...\n"
        " <test_module>,__all__\n"
        " ...\n"
        'how we use the stats will be based on option "--use-specified-test-cases-by".',
    )
    parser.add_argument(
        "--use-specified-test-cases-by",
        type=str,
        choices=["include", "bring-to-front"],
        default="include",
        help='used together with option "--run-specified-test-cases". When specified test case '
        "file is set, this option allows the user to control whether to only run the specified test "
        "modules or to simply bring the specified modules to front and also run the remaining "
        "modules. Note: regardless of this option, we will only run the specified test cases "
        " within a specified test module. For unspecified test modules with the bring-to-front "
        "option, all test cases will be run, as one may expect.",
    )
    return parser.parse_args()
