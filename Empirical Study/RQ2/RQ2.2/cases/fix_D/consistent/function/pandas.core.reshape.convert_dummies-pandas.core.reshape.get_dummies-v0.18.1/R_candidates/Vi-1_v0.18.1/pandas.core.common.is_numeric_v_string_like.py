def is_numeric_v_string_like(a, b):
    """
    numpy doesn't like to compare numeric arrays vs scalar string-likes

    return a boolean result if this is the case for a,b or b,a

    """
    is_a_array = isinstance(a, np.ndarray)
    is_b_array = isinstance(b, np.ndarray)

    is_a_numeric_array = is_a_array and is_numeric_dtype(a)
    is_b_numeric_array = is_b_array and is_numeric_dtype(b)
    is_a_string_array = is_a_array and is_string_like_dtype(a)
    is_b_string_array = is_b_array and is_string_like_dtype(b)

    is_a_scalar_string_like = not is_a_array and is_string_like(a)
    is_b_scalar_string_like = not is_b_array and is_string_like(b)

    return ((is_a_numeric_array and is_b_scalar_string_like) or
            (is_b_numeric_array and is_a_scalar_string_like) or
            (is_a_numeric_array and is_b_string_array) or
            (is_b_numeric_array and is_a_string_array))
