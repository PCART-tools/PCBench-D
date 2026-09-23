@contextlib.contextmanager
def create_export_diagnostic_context() -> Generator[
    infra.DiagnosticContext, None, None
]:
    """Create a diagnostic context for export.

    This is a workaround for code robustness since diagnostic context is accessed by
    export internals via global variable. See `ExportDiagnosticEngine` for more details.
    """
    global _context
    assert _context == engine.background_context, (
        "Export context is already set. Nested export is not supported."
    )
    _context = engine.create_diagnostic_context(
        "torch.onnx.export",
        torch.__version__,
    )
    try:
        yield _context
    finally:
        _context = engine.background_context
