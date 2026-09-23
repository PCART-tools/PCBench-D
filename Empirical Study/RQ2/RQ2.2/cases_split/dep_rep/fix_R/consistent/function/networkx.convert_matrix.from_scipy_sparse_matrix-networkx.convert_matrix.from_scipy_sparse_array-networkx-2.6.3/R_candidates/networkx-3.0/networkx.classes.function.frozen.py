def frozen(*args, **kwargs):
    """Dummy method for raising errors when trying to modify frozen graphs"""
    raise nx.NetworkXError("Frozen graph can't be modified")
