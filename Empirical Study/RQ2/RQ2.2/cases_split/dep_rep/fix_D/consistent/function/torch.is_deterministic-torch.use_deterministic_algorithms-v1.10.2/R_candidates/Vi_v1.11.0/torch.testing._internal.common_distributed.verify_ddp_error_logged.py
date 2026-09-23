def verify_ddp_error_logged(model_DDP, err_substr):
    # Verify error was logged in ddp_logging_data.
    ddp_logging_data = model_DDP._get_ddp_logging_data()
    assert "iteration" in ddp_logging_data
    assert "has_error" in ddp_logging_data
    assert "error" in ddp_logging_data
    logging_err = ddp_logging_data["error"]
    # Remove C++ stacktrace if needed.
    actual = (
        err_substr if err_substr.find("\nException raised from ") == -1
        else err_substr.split("\nException raised from ")[0]
    )
    assert actual in logging_err, f"Did not find expected {actual} in ddp logging data error: {logging_err}"
