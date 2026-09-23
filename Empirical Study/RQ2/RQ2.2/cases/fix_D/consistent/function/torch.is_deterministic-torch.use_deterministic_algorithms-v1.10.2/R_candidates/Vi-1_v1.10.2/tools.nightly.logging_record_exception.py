def logging_record_exception(e: BaseException) -> None:
    with open(os.path.join(logging_run_dir(), "exception"), "w") as f:
        f.write(type(e).__name__)
