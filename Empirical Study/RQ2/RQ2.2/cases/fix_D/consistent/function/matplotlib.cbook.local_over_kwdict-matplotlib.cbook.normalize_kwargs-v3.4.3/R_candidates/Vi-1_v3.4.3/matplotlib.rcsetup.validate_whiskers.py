def validate_whiskers(s):
    try:
        return _listify_validator(validate_float, n=2)(s)
    except (TypeError, ValueError):
        try:
            return float(s)
        except ValueError as e:
            raise ValueError("Not a valid whisker value ['range', float, "
                             "(float, float)]") from e
