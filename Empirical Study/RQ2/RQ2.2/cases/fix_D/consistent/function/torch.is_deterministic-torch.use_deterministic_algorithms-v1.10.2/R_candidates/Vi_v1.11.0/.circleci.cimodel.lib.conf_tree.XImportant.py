def XImportant(name):
    """Compact way to write an important (run on PRs) leaf node"""
    return (name, [("important", [X(True)])])
