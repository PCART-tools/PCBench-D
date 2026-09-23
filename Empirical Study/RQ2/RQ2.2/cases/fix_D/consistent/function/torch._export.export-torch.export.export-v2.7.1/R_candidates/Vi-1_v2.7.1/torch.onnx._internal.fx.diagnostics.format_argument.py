def format_argument(obj: Any) -> str:
    formatter = _format_argument.dispatch(type(obj))
    return formatter(obj)
