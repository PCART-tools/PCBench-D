def get_default_value(initial_value, reduction):
    if initial_value is not None:
        return initial_value
    if reduction == "max":
        return -float("Inf")
    elif reduction == "mean":
        return float("nan")
    elif reduction == "min":
        return float("Inf")
    elif reduction == "sum":
        return 0.0
