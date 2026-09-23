def get_raw_profiles_folder() -> str:
    return os.environ.get("RAW_PROFILES_FOLDER", os.path.join(PROFILE_DIR, "raw"))
