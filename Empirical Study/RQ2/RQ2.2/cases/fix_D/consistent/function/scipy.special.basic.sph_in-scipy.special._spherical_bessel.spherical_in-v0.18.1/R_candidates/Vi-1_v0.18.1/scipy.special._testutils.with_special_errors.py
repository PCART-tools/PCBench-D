def with_special_errors(func):
    """
    Enable special function errors (such as underflow, overflow,
    loss of precision, etc.)
    """
    def wrapper(*a, **kw):
        old_filters = list(getattr(warnings, 'filters', []))
        old_errprint = sc.errprint(1)
        warnings.filterwarnings("error", category=sc.SpecialFunctionWarning)
        try:
            return func(*a, **kw)
        finally:
            sc.errprint(old_errprint)
            setattr(warnings, 'filters', old_filters)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
