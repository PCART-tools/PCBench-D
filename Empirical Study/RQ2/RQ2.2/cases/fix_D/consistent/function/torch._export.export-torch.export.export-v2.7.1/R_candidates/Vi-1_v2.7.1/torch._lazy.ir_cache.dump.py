def dump(dot_file_name: str):
    """Dump TrieCache in the dot format"""
    return torch._C._lazy._dump_ir_cache(dot_file_name)
