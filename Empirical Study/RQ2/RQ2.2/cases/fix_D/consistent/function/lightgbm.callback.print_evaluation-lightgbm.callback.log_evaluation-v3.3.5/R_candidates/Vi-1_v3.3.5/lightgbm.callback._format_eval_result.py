def _format_eval_result(value: list, show_stdv: bool = True) -> str:
    """Format metric string."""
    if len(value) == 4:
        return f"{value[0]}'s {value[1]}: {value[2]:g}"
    elif len(value) == 5:
        if show_stdv:
            return f"{value[0]}'s {value[1]}: {value[2]:g} + {value[4]:g}"
        else:
            return f"{value[0]}'s {value[1]}: {value[2]:g}"
    else:
        raise ValueError("Wrong metric value")
