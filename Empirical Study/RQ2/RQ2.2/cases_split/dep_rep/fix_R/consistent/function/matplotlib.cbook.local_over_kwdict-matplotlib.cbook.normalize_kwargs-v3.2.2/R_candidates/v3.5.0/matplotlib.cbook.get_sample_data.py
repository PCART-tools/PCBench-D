def get_sample_data(fname, asfileobj=True, *, np_load=False):
    """
    Return a sample data file.  *fname* is a path relative to the
    :file:`mpl-data/sample_data` directory.  If *asfileobj* is `True`
    return a file object, otherwise just a file path.

    Sample data files are stored in the 'mpl-data/sample_data' directory within
    the Matplotlib package.

    If the filename ends in .gz, the file is implicitly ungzipped.  If the
    filename ends with .npy or .npz, *asfileobj* is True, and *np_load* is
    True, the file is loaded with `numpy.load`.  *np_load* currently defaults
    to False but will default to True in a future release.
    """
    path = _get_data_path('sample_data', fname)
    if asfileobj:
        suffix = path.suffix.lower()
        if suffix == '.gz':
            return gzip.open(path)
        elif suffix in ['.npy', '.npz']:
            if np_load:
                return np.load(path)
            else:
                _api.warn_deprecated(
                    "3.3", message="In a future release, get_sample_data "
                    "will automatically load numpy arrays.  Set np_load to "
                    "True to get the array and suppress this warning.  Set "
                    "asfileobj to False to get the path to the data file and "
                    "suppress this warning.")
                return path.open('rb')
        elif suffix in ['.csv', '.xrc', '.txt']:
            return path.open('r')
        else:
            return path.open('rb')
    else:
        return str(path)
