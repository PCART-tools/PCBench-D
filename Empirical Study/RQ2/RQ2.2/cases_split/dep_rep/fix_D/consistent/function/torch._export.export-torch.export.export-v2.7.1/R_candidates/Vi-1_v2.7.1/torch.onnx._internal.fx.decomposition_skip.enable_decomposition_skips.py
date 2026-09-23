@contextlib.contextmanager
def enable_decomposition_skips(
    export_options: torch.onnx.ExportOptions,
    skips: Sequence[type[DecompSkip]] = _DEFAULT_SKIP_LIST,
):
    """A context manager that enables the decomposition skips.

    The original operator callables that are otherwise decomposed are replaced with custom operators.
    The ONNXScript functions for exporting the custom operators are added to the ONNX registry inside export_options.
    """
    try:
        for skip in skips:
            skip.register(export_options)
        yield
    finally:
        for skip in skips:
            skip.unregister()
