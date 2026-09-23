def print_error(*args: Any) -> None:
    with open(os.path.join(LOG_DIR, "log.txt"), "a+") as log_file:
        print(f"[ERROR] {' '.join(args)}", file=log_file)
