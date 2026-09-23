def cprint(the_color: str, text: str) -> None:
    if should_color():
        print(color(the_color, text))
    else:
        print(text)
