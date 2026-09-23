def _write_array_header(fp, d, version=None):
    """ Write the header for an array and returns the version used

    Parameters
    ----------
    fp : filelike object
    d : dict
        This has the appropriate entries for writing its string representation
        to the header of the file.
    version: tuple or None
        None means use oldest that works
        explicit version will raise a ValueError if the format does not
        allow saving this data.  Default: None
    """
    header = ["{"]
    for key, value in sorted(d.items()):
        # Need to use repr here, since we eval these when reading
        header.append("'%s': %s, " % (key, repr(value)))
    header.append("}")
    header = "".join(header)
    if version is None:
        header = _wrap_header_guess_version(header)
    else:
        header = _wrap_header(header, version)
    fp.write(header)
