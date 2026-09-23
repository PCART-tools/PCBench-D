@lru_cache()
def find_tex_file(filename, format=None):
    """
    Find a file in the texmf tree.

    Calls :program:`kpsewhich` which is an interface to the kpathsea
    library [1]_. Most existing TeX distributions on Unix-like systems use
    kpathsea. It is also available as part of MikTeX, a popular
    distribution on Windows.

    *If the file is not found, an empty string is returned*.

    Parameters
    ----------
    filename : str or path-like
    format : str or bytes
        Used as the value of the ``--format`` option to :program:`kpsewhich`.
        Could be e.g. 'tfm' or 'vf' to limit the search to that type of files.

    References
    ----------
    .. [1] `Kpathsea documentation <http://www.tug.org/kpathsea/>`_
        The library that :program:`kpsewhich` is part of.
    """

    # we expect these to always be ascii encoded, but use utf-8
    # out of caution
    if isinstance(filename, bytes):
        filename = filename.decode('utf-8', errors='replace')
    if isinstance(format, bytes):
        format = format.decode('utf-8', errors='replace')

    if os.name == 'nt':
        # On Windows only, kpathsea can use utf-8 for cmd args and output.
        # The `command_line_encoding` environment variable is set to force it
        # to always use utf-8 encoding.  See Matplotlib issue #11848.
        kwargs = {'env': {**os.environ, 'command_line_encoding': 'utf-8'},
                  'encoding': 'utf-8'}
    else:  # On POSIX, run through the equivalent of os.fsdecode().
        kwargs = {'encoding': sys.getfilesystemencoding(),
                  'errors': 'surrogatescape'}

    cmd = ['kpsewhich']
    if format is not None:
        cmd += ['--format=' + format]
    cmd += [filename]
    try:
        result = cbook._check_and_log_subprocess(cmd, _log, **kwargs)
    except (FileNotFoundError, RuntimeError):
        return ''
    return result.rstrip('\n')
