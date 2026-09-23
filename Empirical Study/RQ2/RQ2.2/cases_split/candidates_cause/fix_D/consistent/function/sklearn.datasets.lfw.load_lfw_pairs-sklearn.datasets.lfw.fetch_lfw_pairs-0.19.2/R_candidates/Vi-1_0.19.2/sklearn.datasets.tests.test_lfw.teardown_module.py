def teardown_module():
    """Test fixture (clean up) run once after all tests of this module"""
    if os.path.isdir(SCIKIT_LEARN_DATA):
        shutil.rmtree(SCIKIT_LEARN_DATA)
    if os.path.isdir(SCIKIT_LEARN_EMPTY_DATA):
        shutil.rmtree(SCIKIT_LEARN_EMPTY_DATA)
