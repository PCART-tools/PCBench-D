def module_has_submodule(package, module_name):
    """See if 'module' is in 'package'."""
    try:
        package_name = package.__name__
        package_path = package.__path__
    except AttributeError:
        # package isn't a package.
        return False

    full_module_name = package_name + '.' + module_name
    try:
        return importlib_find(full_module_name, package_path) is not None
    except (ModuleNotFoundError, AttributeError):
        # When module_name is an invalid dotted path, Python raises
        # ModuleNotFoundError. AttributeError is raised on PY36 (fixed in PY37)
        # if the penultimate part of the path is not a package.
        return False
