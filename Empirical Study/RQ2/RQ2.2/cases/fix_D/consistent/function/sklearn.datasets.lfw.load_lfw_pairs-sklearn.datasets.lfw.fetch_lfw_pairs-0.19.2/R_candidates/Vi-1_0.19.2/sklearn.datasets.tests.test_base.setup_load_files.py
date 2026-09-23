def setup_load_files():
    global TEST_CATEGORY_DIR1
    global TEST_CATEGORY_DIR2
    TEST_CATEGORY_DIR1 = tempfile.mkdtemp(dir=LOAD_FILES_ROOT)
    TEST_CATEGORY_DIR2 = tempfile.mkdtemp(dir=LOAD_FILES_ROOT)
    sample_file = tempfile.NamedTemporaryFile(dir=TEST_CATEGORY_DIR1,
                                              delete=False)
    sample_file.write(b("Hello World!\n"))
    sample_file.close()
