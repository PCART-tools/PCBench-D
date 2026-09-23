def value_to_literal(value):
    if isinstance(value, str):
        # Quotes string and escapes special characters
        return ascii(value)
    else:
        return str(value)
