def add_max_tokens_pragma_to_files(files: List[str], num_max_tokens: int) -> None:
    for filename in files:
        with open(filename, "r+") as f:
            data = f.read()
            data = add_max_tokens_pragma(data, num_max_tokens)

            f.seek(0)
            f.write(data)
            f.truncate()
