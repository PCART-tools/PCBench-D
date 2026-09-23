def is_cusparse_file(rel_filepath):
    if is_pytorch_file(rel_filepath):
        return "sparse" in rel_filepath.lower()
    return False
