def update_coverage(
    coverage_records: List[CoverageRecord],
    interested_folders: List[str],
    platform: TestPlatform,
) -> None:
    for item in coverage_records:
        # extract information for the record
        record = item.to_dict()
        file_path = record["filepath"]
        if not is_intrested_file(file_path, interested_folders, platform):
            continue
        covered_range = record["covered_lines"]
        uncovered_range = record["uncovered_lines"]
        # transform file name: remote/13223/caffe2/aten -> caffe2/aten
        file_path = transform_file_name(file_path, interested_folders, platform)

        # if file not exists, add it into dictionary
        if file_path not in covered_lines:
            covered_lines[file_path] = set()
        if file_path not in uncovered_lines:
            uncovered_lines[file_path] = set()
        # update this file's covered and uncovered lines
        if covered_range is not None:
            covered_lines[file_path].update(covered_range)
        if uncovered_range is not None:
            uncovered_lines[file_path].update(uncovered_range)
