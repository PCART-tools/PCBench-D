def get_size(file_dir: str) -> int:
    try:
        # we should only expect one file, if no, something is wrong
        file_name = glob.glob(os.path.join(file_dir, "*"))[0]
        return os.stat(file_name).st_size
    except Exception:
        logging.exception(f"error getting file from: {file_dir}")
        return 0
