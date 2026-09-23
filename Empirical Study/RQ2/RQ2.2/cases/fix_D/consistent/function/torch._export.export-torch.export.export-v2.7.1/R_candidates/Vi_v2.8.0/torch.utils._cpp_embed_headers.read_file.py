def read_file(fname: Union[Path, str]) -> list[str]:
    with open(fname, encoding="utf-8") as f:
        return f.readlines()
