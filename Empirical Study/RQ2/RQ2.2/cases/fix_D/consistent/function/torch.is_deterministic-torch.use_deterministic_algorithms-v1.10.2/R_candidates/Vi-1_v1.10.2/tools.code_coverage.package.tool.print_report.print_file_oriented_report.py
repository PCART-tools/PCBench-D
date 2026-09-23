def print_file_oriented_report(
    tests_type: TestStatusType,
    coverage: List[CoverageItem],
    covered_summary: int,
    total_summary: int,
    summary_file: IO[str],
    tests: TestList,
    interested_folders: List[str],
    coverage_only: List[str],
) -> None:
    coverage_percentage = print_file_summary(
        covered_summary, total_summary, summary_file
    )
    # print test condition (interested folder / tests that are successsful or failed)
    print_test_condition(
        tests,
        tests_type,
        interested_folders,
        coverage_only,
        summary_file,
        "FILE SUMMARY",
    )
    # print each file's information
    for item in coverage:
        print(
            item[0].ljust(75),
            (str(item[1]) + "%").rjust(10),
            str(item[2]).rjust(10),
            str(item[3]).rjust(10),
            file=summary_file,
        )

    print(f"summary percentage:{coverage_percentage:.2f}%")
