def _safe_pyplot_import():
    """
    Import and return ``pyplot``, correctly setting the backend if one is
    already forced.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:  # Likely due to a framework mismatch.
        current_framework = cbook._get_running_interactive_framework()
        if current_framework is None:
            raise  # No, something else went wrong, likely with the install...
        backend_mapping = {'qt5': 'qt5agg',
                           'qt4': 'qt4agg',
                           'gtk3': 'gtk3agg',
                           'wx': 'wxagg',
                           'tk': 'tkagg',
                           'macosx': 'macosx',
                           'headless': 'agg'}
        backend = backend_mapping[current_framework]
        rcParams["backend"] = mpl.rcParamsOrig["backend"] = backend
        import matplotlib.pyplot as plt  # Now this should succeed.
    return plt
