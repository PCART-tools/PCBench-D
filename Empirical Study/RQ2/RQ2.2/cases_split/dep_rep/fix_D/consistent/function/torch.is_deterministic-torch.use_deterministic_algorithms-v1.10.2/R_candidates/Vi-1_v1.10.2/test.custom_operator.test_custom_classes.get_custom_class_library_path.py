def get_custom_class_library_path():
    library_filename = glob.glob("build/*custom_class*")
    assert (len(library_filename) == 1)
    library_filename = library_filename[0]
    path = os.path.abspath(library_filename)
    assert os.path.exists(path), path
    return path
