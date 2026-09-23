def _set_collect(group, p, barrier_token, columns):
    """ Get new partition dataframe from partd """
    try:
        return p.get(group)
    except ValueError:
        assert columns is not None, columns
        # when unable to get group, create dummy DataFrame
        # which has the same columns as original
        return pd.DataFrame(columns=columns)
