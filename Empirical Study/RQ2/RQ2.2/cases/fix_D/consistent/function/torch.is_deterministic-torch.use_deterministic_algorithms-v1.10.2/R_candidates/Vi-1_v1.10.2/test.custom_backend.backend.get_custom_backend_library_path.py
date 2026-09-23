def get_custom_backend_library_path():
    """
    Get the path to the library containing the custom backend.

    Return:
        The path to the custom backend object, customized by platform.
    """
    if sys.platform.startswith("win32"):
        library_filename = "custom_backend.dll"
    elif sys.platform.startswith("darwin"):
        library_filename = "libcustom_backend.dylib"
    else:
        library_filename = "libcustom_backend.so"
    path = os.path.abspath("build/{}".format(library_filename))
    assert os.path.exists(path), path
    return path
