@deprecated(
    issue=15109,
    useinstead="from sympy.matrices.common import classof",
    deprecated_since_version="1.3")
def classof(A, B):
    from sympy.matrices.common import classof as classof_
    return classof_(A, B)
