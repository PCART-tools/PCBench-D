def is_onnx_diagnostics_log_artifact_enabled() -> bool:
    return torch._logging._internal.log_state.is_artifact_enabled(
        _ONNX_DIAGNOSTICS_ARTIFACT_LOGGER_NAME
    )
