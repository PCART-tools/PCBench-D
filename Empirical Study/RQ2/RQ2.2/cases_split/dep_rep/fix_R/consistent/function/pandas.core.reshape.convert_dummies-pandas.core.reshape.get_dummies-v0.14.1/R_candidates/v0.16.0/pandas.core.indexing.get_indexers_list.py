def get_indexers_list():

    return [
        ('ix',   _IXIndexer),
        ('iloc', _iLocIndexer),
        ('loc',  _LocIndexer),
        ('at',   _AtIndexer),
        ('iat',  _iAtIndexer),
    ]
