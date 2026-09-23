def parse_jsons(
    test_list: TestList, interested_folders: List[str], platform: TestPlatform
) -> None:
    g = os.walk(JSON_FOLDER_BASE_DIR)

    for path, _, file_list in g:
        for file_name in file_list:
            if file_name.endswith(".json"):
                # if compiler is clang, we only analyze related json / when compiler is gcc, we analyze all jsons
                cov_type = detect_compiler_type(platform)
                if cov_type == CompilerType.CLANG and not related_to_test_list(
                    file_name, test_list
                ):
                    continue
                json_file = os.path.join(path, file_name)
                try:
                    coverage_records = parse_json(json_file, platform)
                except RuntimeError:
                    print_error("Fail to load json file: ", json_file)
                    continue
                # collect information from each target's export file and merge them together:
                update_coverage(coverage_records, interested_folders, platform)
