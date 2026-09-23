def get_name(name: str) -> str:
    return name.replace(" ", "_").replace("-", "_").lower()
