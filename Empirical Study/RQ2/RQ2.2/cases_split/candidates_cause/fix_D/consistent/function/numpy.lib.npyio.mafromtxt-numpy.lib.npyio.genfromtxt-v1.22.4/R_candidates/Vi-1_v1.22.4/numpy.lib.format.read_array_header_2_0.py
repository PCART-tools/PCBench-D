def read_array_header_2_0(fp):
    """
    Read an array header from a filelike object using the 2.0 file format
    version.

    This will leave the file object located just after the header.

    .. versionadded:: 1.9.0

    Parameters
    ----------
    fp : filelike object
        A file object or something with a `.read()` method like a file.

    Returns
    -------
    shape : tuple of int
        The shape of the array.
    fortran_order : bool
        The array data will be written out directly if it is either
        C-contiguous or Fortran-contiguous. Otherwise, it will be made
        contiguous before writing it out.
    dtype : dtype
        The dtype of the file's data.

    Raises
    ------
    ValueError
        If the data is invalid.

    """
    return _read_array_header(fp, version=(2, 0))
