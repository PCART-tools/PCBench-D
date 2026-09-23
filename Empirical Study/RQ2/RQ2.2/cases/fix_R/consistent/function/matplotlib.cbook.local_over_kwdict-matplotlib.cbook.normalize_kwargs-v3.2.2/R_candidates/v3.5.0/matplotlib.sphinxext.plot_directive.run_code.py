@_api.deprecated("3.5")
def run_code(code, code_path, ns=None, function_name=None):
    """
    Import a Python module from a path, and run the function given by
    name, if function_name is not None.
    """
    _run_code(unescape_doctest(code), code_path, ns, function_name)
