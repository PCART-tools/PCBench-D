def file_oriented_report(
    tests: TestList,
    tests_type: TestStatusType,
    interested_folders: List[str],
    coverage_only: List[str],
    covered_lines: Dict[str, Set[int]],
    uncovered_lines: Dict[str, Set[int]],
) -> None:
    with open(os.path.join(SUMMARY_FOLDER_DIR, "file_summary"), "w+") as summary_file:
        covered_summary = 0
        total_summary = 0
        coverage = []
        for file_name in covered_lines:
            # get coverage number for this file
            covered_count = len(covered_lines[file_name])
            total_count = covered_count + len(uncovered_lines[file_name])
            try:
                percentage = round(covered_count / total_count * 100, 2)
            except ZeroDivisionError:
                percentage = 0
            # store information in a list to be sorted
            coverage.append((file_name, percentage, covered_count, total_count))
            # update summary
            covered_summary = covered_summary + covered_count
            total_summary = total_summary + total_count
        # sort
        coverage.sort(key=key_by_name)
        coverage.sort(key=key_by_percentage)
        # print
        print_file_oriented_report(
            tests_type,
            coverage,
            covered_summary,
            total_summary,
            summary_file,
            tests,
            interested_folders,
            coverage_only,
        )
