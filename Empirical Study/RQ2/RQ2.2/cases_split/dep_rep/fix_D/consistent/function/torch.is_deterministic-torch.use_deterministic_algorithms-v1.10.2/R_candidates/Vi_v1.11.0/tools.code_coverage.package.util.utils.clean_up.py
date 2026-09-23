def clean_up() -> None:
    # remove profile folder
    remove_folder(PROFILE_DIR)
    sys.exit("Clean Up Successfully!")
