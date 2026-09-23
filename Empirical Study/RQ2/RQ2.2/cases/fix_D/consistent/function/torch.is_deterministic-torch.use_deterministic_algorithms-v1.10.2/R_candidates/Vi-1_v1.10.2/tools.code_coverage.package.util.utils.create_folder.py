def create_folder(*paths: Any) -> None:
    for path in paths:
        os.makedirs(path, exist_ok=True)
