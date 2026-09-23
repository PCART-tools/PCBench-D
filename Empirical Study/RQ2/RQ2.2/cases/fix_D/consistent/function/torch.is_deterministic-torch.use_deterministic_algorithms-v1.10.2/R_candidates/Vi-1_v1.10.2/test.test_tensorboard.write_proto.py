def write_proto(str_to_compare, function_ptr):
    expected_file = get_expected_file(function_ptr)
    with open(expected_file, 'w') as f:
        f.write(str(str_to_compare))
