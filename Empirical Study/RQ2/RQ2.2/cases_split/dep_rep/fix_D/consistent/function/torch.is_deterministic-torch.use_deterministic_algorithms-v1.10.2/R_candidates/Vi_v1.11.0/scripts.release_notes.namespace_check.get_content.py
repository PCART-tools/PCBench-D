def get_content(submod):
    mod = torch
    if submod:
        submod = submod.split(".")
        for name in submod:
            mod = getattr(mod, name)
    content = dir(mod)
    return content
