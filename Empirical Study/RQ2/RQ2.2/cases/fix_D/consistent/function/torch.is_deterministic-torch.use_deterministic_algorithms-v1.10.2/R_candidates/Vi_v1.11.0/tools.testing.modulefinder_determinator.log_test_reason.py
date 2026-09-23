def log_test_reason(file_type: str, filename: str, test: str, options: Any) -> None:
    if options.verbose:
        print_to_stderr(
            "Determination found {} file {} -- running {}".format(
                file_type,
                filename,
                test,
            )
        )
