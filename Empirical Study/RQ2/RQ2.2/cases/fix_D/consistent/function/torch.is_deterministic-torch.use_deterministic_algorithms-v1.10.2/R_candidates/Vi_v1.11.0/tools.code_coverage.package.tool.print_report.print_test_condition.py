def print_test_condition(
    tests: TestList,
    tests_type: TestStatusType,
    interested_folders: List[str],
    coverage_only: List[str],
    summary_file: IO[str],
    summary_type: str,
) -> None:
    print_test_by_type(tests, tests_type["success"], "fully success", summary_file)
    print_test_by_type(tests, tests_type["partial"], "partially success", summary_file)
    print_test_by_type(tests, tests_type["fail"], "failed", summary_file)
    print(
        "\n\nCoverage Collected Over Interested Folders:\n",
        interested_folders,
        file=summary_file,
    )
    print(
        "\n\nCoverage Compilation Flags Only Apply To: \n",
        coverage_only,
        file=summary_file,
    )
    print(
        "\n\n---------------------------------- "
        + summary_type
        + " ----------------------------------",
        file=summary_file,
    )
