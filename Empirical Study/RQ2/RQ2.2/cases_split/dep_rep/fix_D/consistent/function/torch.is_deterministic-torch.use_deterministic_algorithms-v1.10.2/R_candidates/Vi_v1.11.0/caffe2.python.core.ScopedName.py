def ScopedName(name):
    """prefix the name with the current scope."""
    if isinstance(name, binary_type):
        name = name.decode('ascii')
    return scope.CurrentNameScope() + name
