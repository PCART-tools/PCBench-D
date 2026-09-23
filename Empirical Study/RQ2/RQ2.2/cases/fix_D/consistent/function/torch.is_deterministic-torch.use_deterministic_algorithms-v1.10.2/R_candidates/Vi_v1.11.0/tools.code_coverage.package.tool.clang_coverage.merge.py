def merge(test_list: TestList, platform_type: TestPlatform) -> None:
    print("start merge")
    start_time = time.time()
    # find all raw profile under raw_folder and sub-folders
    raw_folder_path = get_raw_profiles_folder()
    g = os.walk(raw_folder_path)
    for path, dir_list, file_list in g:
        # if there is a folder raw/aten/, create corresponding merged folder profile/merged/aten/ if not exists yet
        create_corresponding_folder(
            path, raw_folder_path, dir_list, MERGED_FOLDER_BASE_DIR
        )
        # check if we can find raw profile under this path's folder
        for file_name in file_list:
            if file_name.endswith(".profraw"):
                if not related_to_test_list(file_name, test_list):
                    continue
                print(f"start merge {file_name}")
                raw_file = os.path.join(path, file_name)
                merged_file_name = replace_extension(file_name, ".merged")
                merged_file = os.path.join(
                    MERGED_FOLDER_BASE_DIR,
                    convert_to_relative_path(path, raw_folder_path),
                    merged_file_name,
                )
                merge_target(raw_file, merged_file, platform_type)
    print_time("merge take time: ", start_time, summary_time=True)
