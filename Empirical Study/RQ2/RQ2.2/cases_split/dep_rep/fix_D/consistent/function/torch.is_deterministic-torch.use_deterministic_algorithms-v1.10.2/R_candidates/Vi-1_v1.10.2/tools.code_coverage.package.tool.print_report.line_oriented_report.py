def line_oriented_report(
    tests: TestList,
    tests_type: TestStatusType,
    interested_folders: List[str],
    coverage_only: List[str],
    covered_lines: Dict[str, Set[int]],
    uncovered_lines: Dict[str, Set[int]],
) -> None:
    with open(os.path.join(SUMMARY_FOLDER_DIR, "line_summary"), "w+") as report_file:
        print_test_condition(
            tests,
            tests_type,
            interested_folders,
            coverage_only,
            report_file,
            "LINE SUMMARY",
        )
        for file_name in covered_lines:
            covered = covered_lines[file_name]
            uncovered = uncovered_lines[file_name]
            print(
                f"{file_name}\n  covered lines: {sorted(covered)}\n  unconvered lines:{sorted(uncovered)}",
                file=report_file,
            )
