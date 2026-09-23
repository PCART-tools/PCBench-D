def as_posix(name: str) -> str:
    return name.replace("\\", "/") if IS_WINDOWS else name
