def _validate_date_int_mult(s):
    if s is None:
        return
    s = validate_bool(s)
    import matplotlib.dates as mdates
    mdates._rcParam_helper.set_int_mult(s)
