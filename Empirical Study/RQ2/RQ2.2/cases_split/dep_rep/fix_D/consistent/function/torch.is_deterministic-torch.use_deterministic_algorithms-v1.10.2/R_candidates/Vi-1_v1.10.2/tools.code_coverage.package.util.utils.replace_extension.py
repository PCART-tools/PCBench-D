def replace_extension(filename: str, ext: str) -> str:
    return filename[: filename.rfind(".")] + ext
