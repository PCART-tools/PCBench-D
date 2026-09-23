def make_module_path_relative(abs_path):
    """
    Given an absolute filepath corresponding to a Python module which was
    loaded via normal import mechanisms using sys.path, convert it into
    a relative path relative to one of the Python search paths.
    """

    abs_path = pathlib.Path(abs_path).resolve()

    for path in sys.path:
        try:
            rel_path = abs_path.relative_to(path)
        except ValueError:
            continue
        else:
            return str(rel_path)

    return str(abs_path)
