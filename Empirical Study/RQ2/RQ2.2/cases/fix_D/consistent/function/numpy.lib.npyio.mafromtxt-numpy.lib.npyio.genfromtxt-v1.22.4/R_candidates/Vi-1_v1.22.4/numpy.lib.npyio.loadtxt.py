@set_array_function_like_doc
@set_module('numpy')
def loadtxt(fname, dtype=float, comments='#', delimiter=None,
            converters=None, skiprows=0, usecols=None, unpack=False,
            ndmin=0, encoding='bytes', max_rows=None, *, like=None):
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
    comments : str or sequence of str, optional
        The characters or list of characters used to indicate the start of a
        comment. None implies no comments. For backwards compatibility, byte
        strings will be decoded as 'latin1'. The default is '#'.
    delimiter : str, optional
        The string used to separate values. For backwards compatibility, byte
        strings will be decoded as 'latin1'. The default is whitespace.
    converters : dict, optional
        A dictionary mapping column number to a function that will parse the
        column string into the desired value.  E.g., if column 0 is a date
        string: ``converters = {0: datestr2num}``.  Converters can also be
        used to provide a default value for missing data (but see also
        `genfromtxt`): ``converters = {3: lambda s: float(s.strip() or 0)}``.
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

    This example shows how `converters` can be used to convert a field
    with a trailing minus sign into a negative number.

    >>> s = StringIO('10.01 31.25-\n19.22 64.31\n17.57- 63.94')
    >>> def conv(fld):
    ...     return -float(fld[:-1]) if fld.endswith(b'-') else float(fld)
    ...
    >>> np.loadtxt(s, converters={0: conv, 1: conv})
    array([[ 10.01, -31.25],
           [ 19.22,  64.31],
           [-17.57,  63.94]])
    """

    if like is not None:
        return _loadtxt_with_like(
            fname, dtype=dtype, comments=comments, delimiter=delimiter,
            converters=converters, skiprows=skiprows, usecols=usecols,
            unpack=unpack, ndmin=ndmin, encoding=encoding,
            max_rows=max_rows, like=like
        )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Nested functions used by loadtxt.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def split_line(line: str):
        """Chop off comments, strip, and split at delimiter."""
        for comment in comments:  # Much faster than using a single regex.
            line = line.split(comment, 1)[0]
        line = line.strip('\r\n')
        return line.split(delimiter) if line else []

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Main body of loadtxt.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Check correctness of the values of `ndmin`
    if ndmin not in [0, 1, 2]:
        raise ValueError('Illegal value of ndmin keyword: %s' % ndmin)

    # Type conversions for Py3 convenience
    if comments is not None:
        if isinstance(comments, (str, bytes)):
            comments = [comments]
        comments = [_decode_line(x) for x in comments]
    else:
        comments = []

    if delimiter is not None:
        delimiter = _decode_line(delimiter)

    user_converters = converters

    byte_converters = False
    if encoding == 'bytes':
        encoding = None
        byte_converters = True

    if usecols is not None:
        # Copy usecols, allowing it to be a single int or a sequence of ints.
        try:
            usecols = list(usecols)
        except TypeError:
            usecols = [usecols]
        for i, col_idx in enumerate(usecols):
            try:
                usecols[i] = opindex(col_idx)  # Cast to builtin int now.
            except TypeError as e:
                e.args = (
                    "usecols must be an int or a sequence of ints but "
                    "it contains at least one element of type %s" %
                    type(col_idx),
                    )
                raise
        if len(usecols) > 1:
            usecols_getter = itemgetter(*usecols)
        else:
            # Get an iterable back, even if using a single column.
            usecols_getter = lambda obj, c=usecols[0]: [obj[c]]
    else:
        usecols_getter = None

    # Make sure we're dealing with a proper dtype
    dtype = np.dtype(dtype)
    defconv = _getconv(dtype)

    dtype_types, packer = _loadtxt_flatten_dtype_internal(dtype)

    fh_closing_ctx = contextlib.nullcontext()
    try:
        if isinstance(fname, os_PathLike):
            fname = os_fspath(fname)
        if _is_string_like(fname):
            fh = np.lib._datasource.open(fname, 'rt', encoding=encoding)
            fencoding = getattr(fh, 'encoding', 'latin1')
            line_iter = iter(fh)
            fh_closing_ctx = contextlib.closing(fh)
        else:
            line_iter = iter(fname)
            fencoding = getattr(fname, 'encoding', 'latin1')
            try:
                first_line = next(line_iter)
            except StopIteration:
                pass  # Nothing matters if line_iter is empty.
            else:
                # Put first_line back.
                line_iter = itertools.chain([first_line], line_iter)
                if isinstance(first_line, bytes):
                    # Using latin1 matches _decode_line's behavior.
                    decoder = methodcaller(
                        "decode",
                        encoding if encoding is not None else "latin1")
                    line_iter = map(decoder, line_iter)
    except TypeError as e:
        raise ValueError(
            f"fname must be a string, filehandle, list of strings,\n"
            f"or generator. Got {type(fname)} instead."
        ) from e

    with fh_closing_ctx:

        # input may be a python2 io stream
        if encoding is not None:
            fencoding = encoding
        # we must assume local encoding
        # TODO emit portability warning?
        elif fencoding is None:
            import locale
            fencoding = locale.getpreferredencoding()

        # Skip the first `skiprows` lines
        for i in range(skiprows):
            next(line_iter)

        # Read until we find a line with some values, and use it to determine
        # the need for decoding and estimate the number of columns.
        for first_line in line_iter:
            ncols = len(usecols or split_line(first_line))
            if ncols:
                # Put first_line back.
                line_iter = itertools.chain([first_line], line_iter)
                break
        else:  # End of lines reached
            ncols = len(usecols or [])
            warnings.warn('loadtxt: Empty input file: "%s"' % fname,
                          stacklevel=2)

        line_iter = itertools.islice(line_iter, max_rows)
        lineno_words_iter = filter(
            itemgetter(1),  # item[1] is words; filter skips empty lines.
            enumerate(map(split_line, line_iter), 1 + skiprows))

        # Now that we know ncols, create the default converters list, and
        # set packing, if necessary.
        if len(dtype_types) > 1:
            # We're dealing with a structured array, each field of
            # the dtype matches a column
            converters = [_getconv(dt) for dt in dtype_types]
        else:
            # All fields have the same dtype; use specialized packers which are
            # much faster than those using _loadtxt_pack_items.
            converters = [defconv for i in range(ncols)]
            if ncols == 1:
                packer = itemgetter(0)
            else:
                def packer(row): return row

        # By preference, use the converters specified by the user
        for i, conv in (user_converters or {}).items():
            if usecols:
                try:
                    i = usecols.index(i)
                except ValueError:
                    # Unused converter specified
                    continue
            if byte_converters:
                # converters may use decode to workaround numpy's old
                # behaviour, so encode the string again (converters are only
                # called with strings) before passing to the user converter.
                def tobytes_first(conv, x):
                    return conv(x.encode("latin1"))
                converters[i] = functools.partial(tobytes_first, conv)
            else:
                converters[i] = conv

        fencode = methodcaller("encode", fencoding)
        converters = [conv if conv is not bytes else fencode
                      for conv in converters]
        if len(set(converters)) == 1:
            # Optimize single-type data. Note that this is only reached if
            # `_getconv` returns equal callables (i.e. not local lambdas) on
            # equal dtypes.
            def convert_row(vals, _conv=converters[0]):
                return [*map(_conv, vals)]
        else:
            def convert_row(vals):
                return [conv(val) for conv, val in zip(converters, vals)]

        # read data in chunks and fill it into an array via resize
        # over-allocating and shrinking the array later may be faster but is
        # probably not relevant compared to the cost of actually reading and
        # converting the data
        X = None
        while True:
            chunk = []
            for lineno, words in itertools.islice(
                    lineno_words_iter, _loadtxt_chunksize):
                if usecols_getter is not None:
                    words = usecols_getter(words)
                elif len(words) != ncols:
                    raise ValueError(
                        f"Wrong number of columns at line {lineno}")
                # Convert each value according to its column, then pack it
                # according to the dtype's nesting, and store it.
                chunk.append(packer(convert_row(words)))
            if not chunk:  # The islice is empty, i.e. we're done.
                break

            if X is None:
                X = np.array(chunk, dtype)
            else:
                nshape = list(X.shape)
                pos = nshape[0]
                nshape[0] += len(chunk)
                X.resize(nshape, refcheck=False)
                X[pos:, ...] = chunk

    if X is None:
        X = np.array([], dtype)

    # Multicolumn data are returned with shape (1, N, M), i.e.
    # (1, 1, M) for a single row - remove the singleton dimension there
    if X.ndim == 3 and X.shape[:2] == (1, 1):
        X.shape = (1, -1)

    # Verify that the array has at least dimensions `ndmin`.
    # Tweak the size and shape of the arrays - remove extraneous dimensions
    if X.ndim > ndmin:
        X = np.squeeze(X)
    # and ensure we have the minimum number of dimensions asked for
    # - has to be in this order for the odd case ndmin=1, X.squeeze().ndim=0
    if X.ndim < ndmin:
        if ndmin == 1:
            X = np.atleast_1d(X)
        elif ndmin == 2:
            X = np.atleast_2d(X).T

    if unpack:
        if len(dtype_types) > 1:
            # For structured arrays, return an array for each field.
            return [X[field] for field in dtype.names]
        else:
            return X.T
    else:
        return X
