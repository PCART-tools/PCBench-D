def _validate_date_like_dtype(dtype):
    try:
        typ = np.datetime_data(dtype)[0]
    except ValueError as e:
        raise TypeError('%s' % e)
    if typ != 'generic' and typ != 'ns':
        raise ValueError('%r is too specific of a frequency, try passing %r'
                         % (dtype.name, dtype.type.__name__))
