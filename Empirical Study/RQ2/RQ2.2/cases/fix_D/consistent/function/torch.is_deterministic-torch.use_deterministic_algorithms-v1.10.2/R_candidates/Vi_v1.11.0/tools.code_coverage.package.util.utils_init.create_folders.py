def create_folders() -> None:
    create_folder(
        PROFILE_DIR,
        MERGED_FOLDER_BASE_DIR,
        JSON_FOLDER_BASE_DIR,
        get_raw_profiles_folder(),
        SUMMARY_FOLDER_DIR,
        LOG_DIR,
    )
