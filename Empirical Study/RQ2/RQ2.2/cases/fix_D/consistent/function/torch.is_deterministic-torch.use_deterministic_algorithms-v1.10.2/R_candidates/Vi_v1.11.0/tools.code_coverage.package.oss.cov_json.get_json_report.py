def get_json_report(test_list: TestList, options: Option) -> None:
    cov_type = detect_compiler_type()
    check_compiler_type(cov_type)
    if cov_type == CompilerType.CLANG:
        # run
        if options.need_run:
            clang_run(test_list)
        # merge && export
        if options.need_merge:
            clang_coverage.merge(test_list, TestPlatform.OSS)
        if options.need_export:
            clang_coverage.export(test_list, TestPlatform.OSS)
    elif cov_type == CompilerType.GCC:
        # run
        if options.need_run:
            gcc_run(test_list)
