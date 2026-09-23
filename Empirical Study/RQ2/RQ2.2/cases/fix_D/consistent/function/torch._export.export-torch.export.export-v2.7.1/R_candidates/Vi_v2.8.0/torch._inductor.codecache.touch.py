def touch(filename: str) -> None:
    open(filename, "a").close()
