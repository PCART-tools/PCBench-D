def color(the_color: str, text: str) -> str:
    if should_color():
        return col.BOLD + the_color + str(text) + col.RESET
    else:
        return text
