def strip_max_tokens_pragma_from_files(files: List[str]) -> None:
    for filename in files:
        with open(filename, "r+") as f:
            data = f.read()
            data = strip_max_tokens_pragmas(data)

            f.seek(0)
            f.write(data)
            f.truncate()
