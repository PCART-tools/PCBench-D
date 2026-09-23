def print_log(*args: Any) -> None:
    with open(os.path.join(LOG_DIR, "log.txt"), "a+") as log_file:
        print(f"[LOG] {' '.join(args)}", file=log_file)
