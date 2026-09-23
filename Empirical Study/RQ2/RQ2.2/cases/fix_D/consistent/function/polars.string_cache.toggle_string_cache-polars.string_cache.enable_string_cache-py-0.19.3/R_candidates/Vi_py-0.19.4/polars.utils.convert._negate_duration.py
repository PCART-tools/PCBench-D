def _negate_duration(duration: str) -> str:
    if duration.startswith("-"):
        return duration[1:]
    return f"-{duration}"
