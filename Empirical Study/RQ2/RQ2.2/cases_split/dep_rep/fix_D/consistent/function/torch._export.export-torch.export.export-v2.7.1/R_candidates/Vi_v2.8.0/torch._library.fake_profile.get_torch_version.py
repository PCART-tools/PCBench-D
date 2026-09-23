def get_torch_version() -> str:
    version = torch.__version__.split(".")
    return f"{int(version[0])}.{int(version[1])}"
