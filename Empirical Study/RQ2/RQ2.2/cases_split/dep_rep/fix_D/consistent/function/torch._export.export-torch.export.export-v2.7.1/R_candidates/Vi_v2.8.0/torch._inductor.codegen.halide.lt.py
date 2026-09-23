def lt(left, right):
    if V.graph.sizevars.statically_known_lt(left, right):
        return True
    try:
        a = V.graph.sizevars.size_hint(left)
        b = V.graph.sizevars.size_hint(right)
    except TypeError:  # unbacked symints
        gcd = sympy.gcd(left, right)
        if gcd == left:
            return left != right
        return False
    if a < b:
        V.graph.sizevars.guard_lt(left, right)
    return a < b
