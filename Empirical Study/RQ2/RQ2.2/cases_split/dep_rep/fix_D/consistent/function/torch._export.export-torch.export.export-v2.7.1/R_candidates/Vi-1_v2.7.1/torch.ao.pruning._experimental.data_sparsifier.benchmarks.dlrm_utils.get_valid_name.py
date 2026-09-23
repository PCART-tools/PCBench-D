def get_valid_name(name):
    """Replaces '.' with '_' as names with '.' are invalid in data sparsifier"""
    return name.replace(".", "_")
