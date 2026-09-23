def get_key_index_source(source, index):
    return f"list(dict.keys({source}))[{index}]"
