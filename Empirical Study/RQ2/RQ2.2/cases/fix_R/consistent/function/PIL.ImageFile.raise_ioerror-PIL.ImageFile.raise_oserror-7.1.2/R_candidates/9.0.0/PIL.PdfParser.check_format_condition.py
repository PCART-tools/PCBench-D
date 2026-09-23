def check_format_condition(condition, error_message):
    if not condition:
        raise PdfFormatError(error_message)
