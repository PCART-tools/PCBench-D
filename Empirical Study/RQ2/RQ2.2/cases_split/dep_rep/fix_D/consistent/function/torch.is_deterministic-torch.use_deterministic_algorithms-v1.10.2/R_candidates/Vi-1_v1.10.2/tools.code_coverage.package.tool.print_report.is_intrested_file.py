def is_intrested_file(file_path: str, interested_folders: List[str]) -> bool:
    if "cuda" in file_path:
        return False
    if "aten/gen_aten" in file_path or "aten/aten_" in file_path:
        return False
    for folder in interested_folders:
        if folder in file_path:
            return True
    return False
