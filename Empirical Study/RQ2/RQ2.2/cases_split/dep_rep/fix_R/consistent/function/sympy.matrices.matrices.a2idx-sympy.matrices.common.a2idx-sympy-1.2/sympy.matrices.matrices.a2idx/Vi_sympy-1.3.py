@deprecated(
    issue=15109,
    deprecated_since_version="1.3",
    useinstead="from sympy.matrices.common import a2idx")
def a2idx(j, n=None):
    from sympy.matrices.common import a2idx as a2idx_
    return a2idx_(j, n)
