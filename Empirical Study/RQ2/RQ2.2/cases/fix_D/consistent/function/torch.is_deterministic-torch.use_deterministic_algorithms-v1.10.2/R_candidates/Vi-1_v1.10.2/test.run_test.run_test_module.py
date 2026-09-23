def run_test_module(test: str, test_directory: str, options) -> Optional[str]:
    test_module = parse_test_module(test)

    # Printing the date here can help diagnose which tests are slow
    print_to_stderr("Running {} ... [{}]".format(test, datetime.now()))
    handler = CUSTOM_HANDLERS.get(test_module, run_test)
    return_code = handler(test_module, test_directory, options)
    assert isinstance(return_code, int) and not isinstance(
        return_code, bool
    ), "Return code should be an integer"
    if return_code == 0:
        return None

    message = f"{test} failed!"
    if return_code < 0:
        # subprocess.Popen returns the child process' exit signal as
        # return code -N, where N is the signal number.
        signal_name = SIGNALS_TO_NAMES_DICT[-return_code]
        message += f" Received signal: {signal_name}"
    return message
