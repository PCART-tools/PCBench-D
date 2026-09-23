def is_shared_lib(file: str) -> bool:
    return file.endswith((".so", ".dll"))
