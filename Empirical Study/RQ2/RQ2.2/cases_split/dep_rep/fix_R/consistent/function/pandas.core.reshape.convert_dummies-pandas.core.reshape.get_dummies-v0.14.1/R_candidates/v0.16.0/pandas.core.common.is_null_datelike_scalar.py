def is_null_datelike_scalar(other):
    """ test whether the object is a null datelike, e.g. Nat
    but guard against passing a non-scalar """
    if other is pd.NaT or other is None:
        return True
    elif np.isscalar(other):

        # a timedelta
        if hasattr(other,'dtype'):
            return other.view('i8') == tslib.iNaT
        elif is_integer(other) and other == tslib.iNaT:
            return True
        return isnull(other)
    return False
