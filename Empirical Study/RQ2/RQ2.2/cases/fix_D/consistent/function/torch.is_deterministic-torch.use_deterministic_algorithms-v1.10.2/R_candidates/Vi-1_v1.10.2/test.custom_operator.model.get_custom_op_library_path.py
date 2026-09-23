def get_custom_op_library_path():
    if sys.platform.startswith("win32"):
        library_filename = "custom_ops.dll"
    elif sys.platform.startswith("darwin"):
        library_filename = "libcustom_ops.dylib"
    else:
        library_filename = "libcustom_ops.so"
    path = os.path.abspath("build/{}".format(library_filename))
    assert os.path.exists(path), path
    return path
