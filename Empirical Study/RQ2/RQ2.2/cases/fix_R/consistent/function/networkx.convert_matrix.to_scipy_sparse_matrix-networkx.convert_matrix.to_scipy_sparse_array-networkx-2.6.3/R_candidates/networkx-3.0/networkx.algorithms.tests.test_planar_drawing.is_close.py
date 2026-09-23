def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    # Check if float numbers are basically equal, for python >=3.5 there is
    # function for that in the standard library
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
