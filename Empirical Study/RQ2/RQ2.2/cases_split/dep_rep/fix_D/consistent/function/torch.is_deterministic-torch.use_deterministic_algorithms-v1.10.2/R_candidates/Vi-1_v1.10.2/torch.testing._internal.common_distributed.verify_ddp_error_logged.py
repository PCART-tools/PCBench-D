def verify_ddp_error_logged(model_DDP, err_substr):
    # Verify error was logged in ddp_logging_data.
    ddp_logging_data = model_DDP._get_ddp_logging_data()
    assert "has_error" in ddp_logging_data
    assert "error" in ddp_logging_data
    assert err_substr in ddp_logging_data["error"]
