def remove_na(series):
    """
    Return series containing only true/non-NaN values, possibly empty.
    """
    return series[notnull(_values_from_object(series))]
