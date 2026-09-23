@contextmanager
def filetexts(d, open=open, mode='t', use_tmpdir=True):
    """ Dumps a number of textfiles to disk

    d - dict
        a mapping from filename to text like {'a.csv': '1,1\n2,2'}

    Since this is meant for use in tests, this context manager will
    automatically switch to a temporary current directory, to avoid
    race conditions when running tests in parallel.
    """
    with (tmp_cwd() if use_tmpdir else noop_context()):
        for filename, text in d.items():
            f = open(filename, 'w' + mode)
            try:
                f.write(text)
            finally:
                try:
                    f.close()
                except AttributeError:
                    pass

        yield list(d)

        for filename in d:
            if os.path.exists(filename):
                with ignoring(OSError):
                    os.remove(filename)
