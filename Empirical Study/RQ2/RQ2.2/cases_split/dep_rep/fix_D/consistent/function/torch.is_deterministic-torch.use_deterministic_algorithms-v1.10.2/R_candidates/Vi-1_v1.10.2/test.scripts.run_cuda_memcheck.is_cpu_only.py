def is_cpu_only(name):
    name = name.lower()
    return ('cpu' in name) and not ('cuda' in name)
