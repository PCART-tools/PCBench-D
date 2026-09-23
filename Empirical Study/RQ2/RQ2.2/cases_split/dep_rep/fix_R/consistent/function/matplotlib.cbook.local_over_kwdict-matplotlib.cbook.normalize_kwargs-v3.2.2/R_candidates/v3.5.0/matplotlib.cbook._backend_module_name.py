def _backend_module_name(name):
    """
    Convert a backend name (either a standard backend -- "Agg", "TkAgg", ... --
    or a custom backend -- "module://...") to the corresponding module name).
    """
    return (name[9:] if name.startswith("module://")
            else "matplotlib.backends.backend_{}".format(name.lower()))
