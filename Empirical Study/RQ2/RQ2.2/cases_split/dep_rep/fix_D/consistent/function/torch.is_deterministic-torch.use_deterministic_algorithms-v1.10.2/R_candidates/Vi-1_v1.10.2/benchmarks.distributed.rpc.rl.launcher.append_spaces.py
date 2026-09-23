def append_spaces(string, length):
    r"""
    Returns a modified string with spaces appended to the end.  If length of string argument
    is greater than or equal to length, a single space is appended, otherwise x spaces are appended
    where x is the difference between the length of string and the length argument
    Args:
        string (str): String to be modified
        length (int): Size of desired return string with spaces appended
    Return: (str)
    """
    string = str(string)
    offset = length - len(string)
    if offset <= 0:
        offset = 1
    string += ' ' * offset
    return string
