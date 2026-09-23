def snapshot_verbose_logging_enabled():
    return torch._logging._internal.log_state.is_artifact_enabled(
        "compiled_autograd_verbose"
    )
