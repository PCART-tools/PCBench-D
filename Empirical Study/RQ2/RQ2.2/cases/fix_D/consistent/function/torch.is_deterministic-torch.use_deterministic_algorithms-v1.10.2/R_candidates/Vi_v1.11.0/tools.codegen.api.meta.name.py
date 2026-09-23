def name(g: NativeFunctionsGroup) -> str:
    # use the overload name from the functional version
    return str(g.functional.func.name).replace('.', '_')
