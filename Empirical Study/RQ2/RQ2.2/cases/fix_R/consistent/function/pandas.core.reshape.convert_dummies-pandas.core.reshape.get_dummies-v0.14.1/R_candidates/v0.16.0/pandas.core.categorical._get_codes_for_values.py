def _get_codes_for_values(values, categories):
    """"
    utility routine to turn values into codes given the specified categories
    """

    from pandas.core.algorithms import _get_data_algo, _hashtables
    if values.dtype != categories.dtype:
        values = _ensure_object(values)
        categories = _ensure_object(categories)
    (hash_klass, vec_klass), vals = _get_data_algo(values, _hashtables)
    t = hash_klass(len(categories))
    t.map_locations(_values_from_object(categories))
    return _coerce_indexer_dtype(t.lookup(values), categories)
