def namespace_filter(data):
    out = set(d for d in data if d[0] != "_")
    return out
