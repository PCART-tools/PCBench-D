def remove_file(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
