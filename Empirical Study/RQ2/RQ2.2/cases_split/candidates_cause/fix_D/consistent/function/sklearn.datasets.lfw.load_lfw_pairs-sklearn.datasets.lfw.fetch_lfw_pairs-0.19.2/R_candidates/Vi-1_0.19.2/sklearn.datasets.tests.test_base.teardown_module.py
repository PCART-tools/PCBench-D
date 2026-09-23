def teardown_module():
    """Test fixture (clean up) run once after all tests of this module"""
    for path in [DATA_HOME, LOAD_FILES_ROOT]:
        _remove_dir(path)
