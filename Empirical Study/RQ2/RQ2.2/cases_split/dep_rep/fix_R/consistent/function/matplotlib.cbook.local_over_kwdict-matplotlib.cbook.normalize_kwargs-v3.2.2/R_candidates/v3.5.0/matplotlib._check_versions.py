def _check_versions():

    # Quickfix to ensure Microsoft Visual C++ redistributable
    # DLLs are loaded before importing kiwisolver
    from . import ft2font

    for modname, minver in [
            ("cycler", "0.10"),
            ("dateutil", "2.7"),
            ("kiwisolver", "1.0.1"),
            ("numpy", "1.17"),
            ("pyparsing", "2.2.1"),
    ]:
        module = importlib.import_module(modname)
        if parse_version(module.__version__) < parse_version(minver):
            raise ImportError(f"Matplotlib requires {modname}>={minver}; "
                              f"you have {module.__version__}")
