def run_test(
    test_module, test_directory, options, launcher_cmd=None, extra_unittest_args=None
):
    unittest_args = options.additional_unittest_args.copy()
    if options.verbose:
        unittest_args.append(f'-{"v"*options.verbose}')  # in case of pytest
    if test_module in RUN_PARALLEL_BLOCKLIST:
        unittest_args = [
            arg for arg in unittest_args if not arg.startswith("--run-parallel")
        ]
    if extra_unittest_args:
        assert isinstance(extra_unittest_args, list)
        unittest_args.extend(extra_unittest_args)

    # If using pytest, replace -f with equivalent -x
    if options.pytest:
        unittest_args = [arg if arg != "-f" else "-x" for arg in unittest_args]
    elif IS_IN_CI:
        # use the downloaded test cases configuration, not supported in pytest
        unittest_args.extend(["--import-slow-tests", "--import-disabled-tests"])

    # Multiprocessing related tests cannot run with coverage.
    # Tracking issue: https://github.com/pytorch/pytorch/issues/50661
    disable_coverage = (
        sys.platform == "win32" and test_module in WINDOWS_COVERAGE_BLOCKLIST
    )

    # Extra arguments are not supported with pytest
    executable = get_executable_command(
        options, allow_pytest=not extra_unittest_args, disable_coverage=disable_coverage
    )

    # TODO: move this logic into common_utils.py instead of passing in "-k" individually
    # The following logic for running specified tests will only run for non-distributed tests, as those are dispatched
    # to test_distributed and not run_test (this function)
    if options.run_specified_test_cases:
        unittest_args.extend(get_test_case_args(test_module, "pytest" in executable))

    # Can't call `python -m unittest test_*` here because it doesn't run code
    # in `if __name__ == '__main__': `. So call `python test_*.py` instead.
    argv = [test_module + ".py"] + unittest_args

    command = (launcher_cmd or []) + executable + argv
    print_to_stderr("Executing {} ... [{}]".format(command, datetime.now()))
    return shell(command, test_directory)
