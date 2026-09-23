def is_recompiles_verbose_enabled():
    return torch._logging._internal.log_state.is_artifact_enabled("recompiles_verbose")
