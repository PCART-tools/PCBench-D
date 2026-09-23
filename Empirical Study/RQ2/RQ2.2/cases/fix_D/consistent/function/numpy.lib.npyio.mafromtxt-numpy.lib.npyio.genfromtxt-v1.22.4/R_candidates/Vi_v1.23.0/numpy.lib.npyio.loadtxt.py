@set_array_function_like_doc
@set_module('numpy')
def loadtxt(fname, dtype=float, comments='#', delimiter=None,
            converters=None, skiprows=0, usecols=None, unpack=False,
            ndmin=0, encoding='bytes', max_rows=None, *, quotechar=None,
            like=None):
    r"""
    Load data from a text file.

    Each row in the text file must have the same number of values.

    Parameters
    ----------
    fname : file, str, pathlib.Path, list of str, generator
        File, filename, list, or generator to read.  If the filename
        extension is ``.gz`` or ``.bz2``, the file is first decompressed. Note
        that generators must return bytes or strings. The strings
        in a list or produced by a generator are treated as lines.
    dtype : data-type, optional
        Data-type of the resulting array; default: float.  If this is a
        structured data-type, the resulting array will be 1-dimensional, and
        each row will be interpreted as an element of the array.  In this
        case, the number of columns used must match the number of fields in
        the data-type.
    comments : str or sequence of str or None, optional
        The characters or list of characters used to indicate the start of a
        comment. None implies no comments. For backwards compatibility, byte
        strings will be decoded as 'latin1'. The default is '#'.
    delimiter : str, optional
        The string used to separate values. For backwards compatibility, byte
        strings will be decoded as 'latin1'. The default is whitespace.
    converters : dict or callable, optional
        A function to parse all columns strings into the desired value, or
        a dictionary mapping column number to a parser function.
        E.g. if column 0 is a date string: ``converters = {0: datestr2num}``.
        Converters can also be used to provide a default value for missing
        data, e.g. ``converters = lambda s: float(s.strip() or 0)`` will
        convert empty fields to 0.
        Default: None.
    skiprows : int, optional
        Skip the first `skiprows` lines, including comments; default: 0.
    usecols : int or sequence, optional
        Which columns to read, with 0 being the first. For example,
        ``usecols = (1,4,5)`` will extract the 2nd, 5th and 6th columns.
        The default, None, results in all columns being read.

        .. versionchanged:: 1.11.0
            When a single column has to be read it is possible to use
            an integer instead of a tuple. E.g ``usecols = 3`` reads the
            fourth column the same way as ``usecols = (3,)`` would.
    unpack : bool, optional
        If True, the returned array is transposed, so that arguments may be
        unpacked using ``x, y, z = loadtxt(...)``.  When used with a
        structured data-type, arrays are returned for each field.
        Default is False.
    ndmin : int, optional
        The returned array will have at least `ndmin` dimensions.
        Otherwise mono-dimensional axes will be squeezed.
        Legal values: 0 (default), 1 or 2.

        .. versionadded:: 1.6.0
    encoding : str, optional
        Encoding used to decode the inputfile. Does not apply to input streams.
        The special value 'bytes' enables backward compatibility workarounds
        that ensures you receive byte arrays as results if possible and passes
        'latin1' encoded strings to converters. Override this value to receive
        unicode arrays and pass strings as input to converters.  If set to None
        the system default is used. The default value is 'bytes'.

        .. versionadded:: 1.14.0
    max_rows : int, optional
        Read `max_rows` lines of content after `skiprows` lines. The default
        is to read all the lines.

        .. versionadded:: 1.16.0
    quotechar : unicode character or None, optional
        The character used to denote the start and end of a quoted item.
        Occurrences of the delimiter or comment characters are ignored within
        a quoted item. The default value is ``quotechar=None``, which means
        quoting support is disabled.

        If two consecutive instances of `quotechar` are found within a quoted
        field, the first is treated as an escape character. See examples.

        .. versionadded:: 1.23.0
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Data read from the text file.

    See Also
    --------
    load, fromstring, fromregex
    genfromtxt : Load data with missing values handled as specified.
    scipy.io.loadmat : reads MATLAB data files

    Notes
    -----
    This function aims to be a fast reader for simply formatted files.  The
    `genfromtxt` function provides more sophisticated handling of, e.g.,
    lines with missing values.

    .. versionadded:: 1.10.0

    The strings produced by the Python float.hex method can be used as
    input for floats.

    Examples
    --------
    >>> from io import StringIO   # StringIO behaves like a file object
    >>> c = StringIO("0 1\n2 3")
    >>> np.loadtxt(c)
    array([[0., 1.],
           [2., 3.]])

    >>> d = StringIO("M 21 72\nF 35 58")
    >>> np.loadtxt(d, dtype={'names': ('gender', 'age', 'weight'),
    ...                      'formats': ('S1', 'i4', 'f4')})
    array([(b'M', 21, 72.), (b'F', 35, 58.)],
          dtype=[('gender', 'S1'), ('age', '<i4'), ('weight', '<f4')])

    >>> c = StringIO("1,0,2\n3,0,4")
    >>> x, y = np.loadtxt(c, delimiter=',', usecols=(0, 2), unpack=True)
    >>> x
    array([1., 3.])
    >>> y
    array([2., 4.])

    The `converters` argument is used to specify functions to preprocess the
    text prior to parsing. `converters` can be a dictionary that maps
    preprocessing functions to each column:

    >>> s = StringIO("1.618, 2.296\n3.141, 4.669\n")
    >>> conv = {
    ...     0: lambda x: np.floor(float(x)),  # conversion fn for column 0
    ...     1: lambda x: np.ceil(float(x)),  # conversion fn for column 1
    ... }
    >>> np.loadtxt(s, delimiter=",", converters=conv)
    array([[1., 3.],
           [3., 5.]])

    `converters` can be a callable instead of a dictionary, in which case it
    is applied to all columns:

    >>> s = StringIO("0xDE 0xAD\n0xC0 0xDE")
    >>> import functools
    >>> conv = functools.partial(int, base=16)
    >>> np.loadtxt(s, converters=conv)
    array([[222., 173.],
           [192., 222.]])

    This example shows how `converters` can be used to convert a field
    with a trailing minus sign into a negative number.

    >>> s = StringIO('10.01 31.25-\n19.22 64.31\n17.57- 63.94')
    >>> def conv(fld):
    ...     return -float(fld[:-1]) if fld.endswith(b'-') else float(fld)
    ...
    >>> np.loadtxt(s, converters=conv)
    array([[ 10.01, -31.25],
           [ 19.22,  64.31],
           [-17.57,  63.94]])

    Using a callable as the converter can be particularly useful for handling
    values with different formatting, e.g. floats with underscores:

    >>> s = StringIO("1 2.7 100_000")
    >>> np.loadtxt(s, converters=float)
    array([1.e+00, 2.7e+00, 1.e+05])

    This idea can be extended to automatically handle values specified in
    many different formats:

    >>> def conv(val):
    ...     try:
    ...         return float(val)
    ...     except ValueError:
    ...         return float.fromhex(val)
    >>> s = StringIO("1, 2.5, 3_000, 0b4, 0x1.4000000000000p+2")
    >>> np.loadtxt(s, delimiter=",", converters=conv, encoding=None)
    array([1.0e+00, 2.5e+00, 3.0e+03, 1.8e+02, 5.0e+00])

    Note that with the default ``encoding="bytes"``, the inputs to the
    converter function are latin-1 encoded byte strings. To deactivate the
    implicit encoding prior to conversion, use ``encoding=None``

    >>> s = StringIO('10.01 31.25-\n19.22 64.31\n17.57- 63.94')
    >>> conv = lambda x: -float(x[:-1]) if x.endswith('-') else float(x)
    >>> np.loadtxt(s, converters=conv, encoding=None)
    array([[ 10.01, -31.25],
           [ 19.22,  64.31],
           [-17.57,  63.94]])

    Support for quoted fields is enabled with the `quotechar` parameter.
    Comment and delimiter characters are ignored when they appear within a
    quoted item delineated by `quotechar`:

    >>> s = StringIO('"alpha, #42", 10.0\n"beta, #64", 2.0\n')
    >>> dtype = np.dtype([("label", "U12"), ("value", float)])
    >>> np.loadtxt(s, dtype=dtype, delimiter=",", quotechar='"')
    array([('alpha, #42', 10.), ('beta, #64',  2.)],
          dtype=[('label', '<U12'), ('value', '<f8')])

    Two consecutive quote characters within a quoted field are treated as a
    single escaped character:

    >>> s = StringIO('"Hello, my name is ""Monty""!"')
    >>> np.loadtxt(s, dtype="U", delimiter=",", quotechar='"')
    array('Hello, my name is "Monty"!', dtype='<U26')

    """

    if like is not None:
        return _loadtxt_with_like(
            fname, dtype=dtype, comments=comments, delimiter=delimiter,
            converters=converters, skiprows=skiprows, usecols=usecols,
            unpack=unpack, ndmin=ndmin, encoding=encoding,
            max_rows=max_rows, like=like
        )

    if isinstance(delimiter, bytes):
        delimiter.decode("latin1")

    if dtype is None:
        dtype = np.float64

    comment = comments
    # Control character type conversions for Py3 convenience
    if comment is not None:
        if isinstance(comment, (str, bytes)):
            comment = [comment]
        comment = [
            x.decode('latin1') if isinstance(x, bytes) else x for x in comment]
    if isinstance(delimiter, bytes):
        delimiter = delimiter.decode('latin1')

    arr = _read(fname, dtype=dtype, comment=comment, delimiter=delimiter,
                converters=converters, skiplines=skiprows, usecols=usecols,
                unpack=unpack, ndmin=ndmin, encoding=encoding,
                max_rows=max_rows, quote=quotechar)

    return arr
