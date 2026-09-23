def remove_files() -> None:
    # remove log
    remove_file(os.path.join(LOG_DIR, "log.txt"))
