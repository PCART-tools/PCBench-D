def update_gzip_dict(gzip_dict: Dict[str, int], file_name: str) -> str:
    file_name = file_name.lower()
    gzip_dict[file_name] = gzip_dict.get(file_name, 0) + 1
    num = gzip_dict[file_name]
    return str(num) + "_" + file_name
