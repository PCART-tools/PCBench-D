def _pkl_filepath(*args, **kwargs):
    """Ensure different filenames for Python 2 and Python 3 pickles

    An object pickled under Python 3 cannot be loaded under Python 2. An object
    pickled under Python 2 can sometimes not be loaded correctly under Python 3
    because some Python 2 strings are decoded as Python 3 strings which can be
    problematic for objects that use Python 2 strings as byte buffers for
    numerical data instead of "real" strings.

    Therefore, dataset loaders in scikit-learn use different files for pickles
    manages by Python 2 and Python 3 in the same SCIKIT_LEARN_DATA folder so as
    to avoid conflicts.

    args[-1] is expected to be the ".pkl" filename. Under Python 3, a suffix is
    inserted before the extension to s

    _pkl_filepath('/path/to/folder', 'filename.pkl') returns:
      - /path/to/folder/filename.pkl under Python 2
      - /path/to/folder/filename_py3.pkl under Python 3+

    """
    py3_suffix = kwargs.get("py3_suffix", "_py3")
    basename, ext = splitext(args[-1])
    if sys.version_info[0] >= 3:
        basename += py3_suffix
    new_args = args[:-1] + (basename + ext,)
    return join(*new_args)
