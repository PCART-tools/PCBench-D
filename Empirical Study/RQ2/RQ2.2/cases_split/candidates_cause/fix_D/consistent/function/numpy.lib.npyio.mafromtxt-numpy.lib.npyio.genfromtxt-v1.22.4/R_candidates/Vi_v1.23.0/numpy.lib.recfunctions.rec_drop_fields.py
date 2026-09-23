@array_function_dispatch(_rec_drop_fields_dispatcher)
def rec_drop_fields(base, drop_names):
    """
    Returns a new numpy.recarray with fields in `drop_names` dropped.
    """
    return drop_fields(base, drop_names, usemask=False, asrecarray=True)
