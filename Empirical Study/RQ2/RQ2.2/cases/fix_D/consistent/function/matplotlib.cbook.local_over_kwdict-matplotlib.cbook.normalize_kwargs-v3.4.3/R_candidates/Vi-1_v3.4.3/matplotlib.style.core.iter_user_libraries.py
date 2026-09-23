def iter_user_libraries():
    for stylelib_path in USER_LIBRARY_PATHS:
        stylelib_path = os.path.expanduser(stylelib_path)
        if os.path.exists(stylelib_path) and os.path.isdir(stylelib_path):
            yield stylelib_path
