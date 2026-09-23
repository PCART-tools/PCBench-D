def cached_import(module_path, class_name):
    modules = sys.modules
    if module_path not in modules or (
        # Module is not fully initialized.
        getattr(modules[module_path], '__spec__', None) is not None and
        getattr(modules[module_path].__spec__, '_initializing', False) is True
    ):
        import_module(module_path)
    return getattr(modules[module_path], class_name)
