def _validate_format_argument(format: str | None) -> None:
    if format is not None and ".%f" in format:
        message = (
            "Detected the pattern `.%f` in the chrono format string."
            " This pattern should not be used to parse values after a decimal point."
            " Use `%.f` instead."
            " See the full specification: https://docs.rs/chrono/latest/chrono/format/strftime"
        )
        warnings.warn(
            message, category=ChronoFormatWarning, stacklevel=find_stacklevel()
        )
