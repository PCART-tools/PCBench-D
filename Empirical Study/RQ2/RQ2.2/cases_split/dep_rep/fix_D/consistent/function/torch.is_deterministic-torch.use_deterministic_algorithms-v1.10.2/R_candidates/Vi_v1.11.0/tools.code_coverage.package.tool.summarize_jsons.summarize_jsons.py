def summarize_jsons(
    test_list: TestList,
    interested_folders: List[str],
    coverage_only: List[str],
    platform: TestPlatform,
) -> None:
    start_time = time.time()
    if detect_compiler_type(platform) == CompilerType.GCC:
        html_oriented_report()
    else:
        parse_jsons(test_list, interested_folders, platform)
        update_set()
        line_oriented_report(
            test_list,
            tests_type,
            interested_folders,
            coverage_only,
            covered_lines,
            uncovered_lines,
        )
        file_oriented_report(
            test_list,
            tests_type,
            interested_folders,
            coverage_only,
            covered_lines,
            uncovered_lines,
        )
    print_time("summary jsons take time: ", start_time)
