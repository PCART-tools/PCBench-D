def print_time(message: str, start_time: float, summary_time: bool = False) -> None:
    with open(os.path.join(LOG_DIR, "log.txt"), "a+") as log_file:
        end_time = time.time()
        print(message, convert_time(end_time - start_time), file=log_file)
        if summary_time:
            print("\n", file=log_file)
