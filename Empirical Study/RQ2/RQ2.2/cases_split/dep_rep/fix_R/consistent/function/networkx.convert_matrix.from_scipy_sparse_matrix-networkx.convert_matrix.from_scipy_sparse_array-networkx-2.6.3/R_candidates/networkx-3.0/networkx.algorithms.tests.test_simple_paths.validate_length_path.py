def validate_length_path(G, s, t, soln_len, length, path):
    assert soln_len == length
    validate_path(G, s, t, length, path)
