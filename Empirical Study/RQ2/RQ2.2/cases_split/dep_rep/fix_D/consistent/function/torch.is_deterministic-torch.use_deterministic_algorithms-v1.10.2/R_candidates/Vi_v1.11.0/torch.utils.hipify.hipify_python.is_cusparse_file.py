def is_cusparse_file(filepath):
    if is_pytorch_file(filepath):
        return "sparse" in filepath.lower()
    return False
