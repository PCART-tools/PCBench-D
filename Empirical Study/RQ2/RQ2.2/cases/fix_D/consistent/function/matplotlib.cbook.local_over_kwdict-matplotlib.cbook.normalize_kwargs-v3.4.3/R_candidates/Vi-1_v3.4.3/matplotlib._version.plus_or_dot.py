def plus_or_dot(pieces):
    if "+" in pieces.get("closest-tag", ""):
        return "."
    return "+"
