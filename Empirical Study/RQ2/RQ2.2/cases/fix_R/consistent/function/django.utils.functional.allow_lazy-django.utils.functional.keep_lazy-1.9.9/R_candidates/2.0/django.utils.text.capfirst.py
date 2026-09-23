@keep_lazy_text
def capfirst(x):
    """Capitalize the first letter of a string."""
    return x and str(x)[0].upper() + str(x)[1:]
