def _read_file(filename: str) -> str:
    with open(filename, "rb") as f:
        b = f.read()
        return b.decode("utf-8")
