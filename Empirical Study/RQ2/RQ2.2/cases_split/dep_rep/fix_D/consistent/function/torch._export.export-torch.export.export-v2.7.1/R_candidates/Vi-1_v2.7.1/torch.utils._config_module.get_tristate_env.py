def get_tristate_env(name: str, default: Any = None) -> Optional[bool]:
    value = os.environ.get(name)
    if value == "1":
        return True
    if value == "0":
        return False
    return default
