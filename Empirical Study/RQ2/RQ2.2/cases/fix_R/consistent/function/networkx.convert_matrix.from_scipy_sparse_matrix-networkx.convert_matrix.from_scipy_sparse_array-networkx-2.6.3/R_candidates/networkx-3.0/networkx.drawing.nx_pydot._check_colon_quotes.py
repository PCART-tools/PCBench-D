def _check_colon_quotes(s):
    # A quick helper function to check if a string has a colon in it
    # and if it is quoted properly with double quotes.
    # refer https://github.com/pydot/pydot/issues/258
    return ":" in s and (s[0] != '"' or s[-1] != '"')
