def _add_data_doc(docstring, replace_names):
    """
    Add documentation for a *data* field to the given docstring.

    Parameters
    ----------
    docstring : str
        The input docstring.
    replace_names : list of str or None
        The list of parameter names which arguments should be replaced by
        ``data[name]`` (if ``data[name]`` does not throw an exception).  If
        None, replacement is attempted for all arguments.

    Returns
    -------
    str
        The augmented docstring.
    """
    if (docstring is None
            or replace_names is not None and len(replace_names) == 0):
        return docstring
    docstring = inspect.cleandoc(docstring)
    repl = (
        ("    every other argument can also be string ``s``, which is\n"
         "    interpreted as ``data[s]`` (unless this raises an exception).")
        if replace_names is None else
        ("    the following arguments can also be string ``s``, which is\n"
         "    interpreted as ``data[s]`` (unless this raises an exception):\n"
         "    " + ", ".join(map("*{}*".format, replace_names))) + ".")
    addendum = _DATA_DOC_APPENDIX.format(replaced=repl)
    if _DATA_DOC_TITLE not in docstring:
        addendum = _DATA_DOC_TITLE + addendum
    return docstring + addendum
