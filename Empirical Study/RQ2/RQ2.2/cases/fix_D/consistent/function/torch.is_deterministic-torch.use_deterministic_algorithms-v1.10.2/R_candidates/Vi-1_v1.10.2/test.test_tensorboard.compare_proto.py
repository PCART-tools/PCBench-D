def compare_proto(str_to_compare, function_ptr):
    expected = read_expected_content(function_ptr)
    str_to_compare = str(str_to_compare)
    return remove_whitespace(str_to_compare) == remove_whitespace(expected)
