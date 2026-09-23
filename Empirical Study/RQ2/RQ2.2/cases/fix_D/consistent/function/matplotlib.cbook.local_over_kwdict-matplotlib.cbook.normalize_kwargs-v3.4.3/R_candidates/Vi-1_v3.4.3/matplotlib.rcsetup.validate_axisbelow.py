def validate_axisbelow(s):
    try:
        return validate_bool(s)
    except ValueError:
        if isinstance(s, str):
            if s == 'line':
                return 'line'
            if s.lower().startswith('line'):
                _api.warn_deprecated(
                    "3.3", message=f"Support for setting axes.axisbelow to "
                    f"{s!r} to mean 'line' is deprecated since %(since)s and "
                    f"will be removed %(removal)s; set it to 'line' instead.")
                return 'line'
    raise ValueError('%s cannot be interpreted as'
                     ' True, False, or "line"' % s)
