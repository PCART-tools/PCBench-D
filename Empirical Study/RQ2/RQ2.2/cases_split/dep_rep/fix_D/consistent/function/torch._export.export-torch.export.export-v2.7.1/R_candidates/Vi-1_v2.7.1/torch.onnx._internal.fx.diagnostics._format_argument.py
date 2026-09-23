@functools.singledispatch
def _format_argument(obj: Any) -> str:
    return formatter.format_argument(obj)
