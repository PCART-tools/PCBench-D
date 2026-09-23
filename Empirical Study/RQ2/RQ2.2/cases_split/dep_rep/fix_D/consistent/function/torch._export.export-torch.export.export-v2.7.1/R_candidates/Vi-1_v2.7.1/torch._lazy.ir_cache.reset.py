def reset():
    """Clear TrieCache. This is needed in testing to avoid
    node reusing between different tests.
    """
    return torch._C._lazy._clear_ir_cache()
