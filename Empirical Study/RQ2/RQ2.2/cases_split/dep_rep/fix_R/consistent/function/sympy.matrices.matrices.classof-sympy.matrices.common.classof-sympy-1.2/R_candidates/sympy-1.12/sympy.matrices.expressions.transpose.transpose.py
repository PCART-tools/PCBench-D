def transpose(expr):
    """Matrix transpose"""
    return Transpose(expr).doit(deep=False)
