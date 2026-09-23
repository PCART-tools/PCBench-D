def diagnose(
    rule: infra.Rule,
    level: infra.Level,
    message: str | None = None,
    frames_to_skip: int = 2,
    **kwargs,
) -> TorchScriptOnnxExportDiagnostic:
    """Creates a diagnostic and record it in the global diagnostic context.

    This is a wrapper around `context.log` that uses the global diagnostic
    context.
    """
    diagnostic = TorchScriptOnnxExportDiagnostic(
        rule, level, message, frames_to_skip=frames_to_skip, **kwargs
    )
    export_context().log(diagnostic)
    return diagnostic
