def read_expected_content(function_ptr):
    expected_file = get_expected_file(function_ptr)
    assert os.path.exists(expected_file)
    with open(expected_file, "r") as f:
        return f.read()
