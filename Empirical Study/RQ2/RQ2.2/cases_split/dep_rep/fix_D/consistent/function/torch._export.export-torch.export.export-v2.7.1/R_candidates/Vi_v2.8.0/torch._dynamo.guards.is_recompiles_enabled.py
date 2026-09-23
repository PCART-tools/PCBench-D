def is_recompiles_enabled():
    return torch._logging._internal.log_state.is_artifact_enabled("recompiles")
