def format_message_in_text(fn: Callable, *args: Any, **kwargs: Any) -> str:
    return f"{formatter.display_name(fn)}. "
