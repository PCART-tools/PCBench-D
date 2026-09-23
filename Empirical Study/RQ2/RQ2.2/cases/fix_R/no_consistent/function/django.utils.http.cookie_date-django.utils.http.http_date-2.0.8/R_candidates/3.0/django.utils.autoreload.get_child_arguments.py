def get_child_arguments():
    """
    Return the executable. This contains a workaround for Windows if the
    executable is reported to not have the .exe extension which can cause bugs
    on reloading.
    """
    import django.__main__

    args = [sys.executable] + ['-W%s' % o for o in sys.warnoptions]
    if sys.argv[0] == django.__main__.__file__:
        # The server was started with `python -m django runserver`.
        args += ['-m', 'django']
        args += sys.argv[1:]
    else:
        args += sys.argv
    return args
