def fuzzy_eq(x: Optional[bool], y: Optional[bool]) -> Optional[bool]:
    if None in (x, y):
        return None
    return x == y
