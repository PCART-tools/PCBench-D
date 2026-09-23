def _MakeList(input):
    """ input is a tuple.
    Example:
    (a, b, c)   --> [a, b, c]
    (a)         --> [a]
    ([a, b, c]) --> [a, b, c]
    """
    if len(input) == 0:
        raise ValueError(
            'input cannot be empty.')
    elif len(input) == 1:
        output = input[0]
        if not isinstance(output, list):
            output = [output]
    else:
        output = list(input)
    return output
