def process_signature(line: str) -> str:
    """
    Given a raw function signature, clean it up by removing the self-referential datapipe argument,
    default arguments of input functions, newlines, and spaces.
    """
    tokens: List[str] = split_outside_bracket(line)
    for i, token in enumerate(tokens):
        tokens[i] = token.strip(' ')
        if token == "cls":
            tokens[i] = "self"
        elif i > 0 and ("self" == tokens[i - 1]) and (tokens[i][0] != "*"):
            # Remove the datapipe after 'self' or 'cls' unless it has '*'
            tokens[i] = ""
        elif "Callable =" in token:  # Remove default argument if it is a function
            head, default_arg = token.rsplit("=", 2)
            tokens[i] = head.strip(' ') + "= ..."
    tokens = [t for t in tokens if t != ""]
    line = ', '.join(tokens)
    return line
