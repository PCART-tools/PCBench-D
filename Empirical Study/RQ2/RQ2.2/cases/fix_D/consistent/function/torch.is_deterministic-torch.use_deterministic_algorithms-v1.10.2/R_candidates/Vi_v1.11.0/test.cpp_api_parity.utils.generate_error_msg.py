def generate_error_msg(name, cpp_value, python_value):
    return (
        "Parity test failed: {} in C++ has value: {}, "
        "which does not match the corresponding value in Python: {}.\n{}").format(
        name, cpp_value, python_value, MESSAGE_HOW_TO_FIX_CPP_PARITY_TEST_FAILURE)
