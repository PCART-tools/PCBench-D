def _validate_date_converter(s):
    if s is None:
        return
    s = validate_string(s)
    if s not in ['auto', 'concise']:
        _api.warn_external(f'date.converter string must be "auto" or '
                           f'"concise", not "{s}".  Check your matplotlibrc')
        return
    import matplotlib.dates as mdates
    mdates._rcParam_helper.set_converter(s)
