def parse_json(json_file: str, platform: TestPlatform) -> List[CoverageRecord]:
    print("start parse:", json_file)
    json_obj, read_status = get_json_obj(json_file)
    if read_status == 0:
        tests_type["success"].add(json_file)
    elif read_status == 1:
        tests_type["partial"].add(json_file)
    else:
        tests_type["fail"].add(json_file)
        raise RuntimeError(
            "Fail to do code coverage! Fail to load json file: ", json_file
        )

    cov_type = detect_compiler_type(platform)

    coverage_records: List[CoverageRecord] = []
    if cov_type == CompilerType.CLANG:
        coverage_records = LlvmCoverageParser(json_obj).parse("fbcode")
        # print(coverage_records)
    elif cov_type == CompilerType.GCC:
        coverage_records = GcovCoverageParser(json_obj).parse()

    return coverage_records
