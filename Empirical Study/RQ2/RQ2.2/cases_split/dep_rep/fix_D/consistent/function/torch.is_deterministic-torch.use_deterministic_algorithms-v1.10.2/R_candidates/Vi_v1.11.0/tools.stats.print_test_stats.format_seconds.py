def format_seconds(seconds: List[float]) -> str:
    if len(seconds) > 0:
        x = list_stat(seconds)
        return f'total time {display_stat(x, ((5, 2), (4, 2)))}'.strip()
    return ''
