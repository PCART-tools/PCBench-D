def sanitize_test_filename(filename):
    # inspect.getfile returns absolute path in some CI jobs, converting it to relative path if needed
    if filename.startswith(CI_TEST_PREFIX):
        filename = filename[len(CI_TEST_PREFIX) + 1:]
    strip_py = re.sub(r'.py$', '', filename)
    return re.sub('/', r'.', strip_py)
