def eq(left, right):
    if V.graph.sizevars.statically_known_equals(left, right):
        return True
    try:
        a = V.graph.sizevars.size_hint(left)
        b = V.graph.sizevars.size_hint(right)
    except TypeError:  # unbacked symints
        return False
    if a == b:
        V.graph.sizevars.guard_equals(left, right)
    return a == b
