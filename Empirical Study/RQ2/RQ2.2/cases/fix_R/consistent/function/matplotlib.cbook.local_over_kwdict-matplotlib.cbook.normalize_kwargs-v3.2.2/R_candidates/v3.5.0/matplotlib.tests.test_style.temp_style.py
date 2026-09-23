@contextmanager
def temp_style(style_name, settings=None):
    """Context manager to create a style sheet in a temporary directory."""
    if not settings:
        settings = DUMMY_SETTINGS
    temp_file = '%s.%s' % (style_name, STYLE_EXTENSION)
    try:
        with TemporaryDirectory() as tmpdir:
            # Write style settings to file in the tmpdir.
            Path(tmpdir, temp_file).write_text(
                "\n".join("{}: {}".format(k, v) for k, v in settings.items()))
            # Add tmpdir to style path and reload so we can access this style.
            USER_LIBRARY_PATHS.append(tmpdir)
            style.reload_library()
            yield
    finally:
        style.reload_library()
