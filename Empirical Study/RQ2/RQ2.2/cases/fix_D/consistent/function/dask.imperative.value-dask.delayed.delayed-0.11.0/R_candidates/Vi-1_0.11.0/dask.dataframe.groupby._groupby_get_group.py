def _groupby_get_group(df, by_key, get_key, columns):
    # SeriesGroupBy may pass df which includes group key
    grouped = df.groupby(by_key)

    if get_key in grouped.groups:
        if isinstance(df, pd.DataFrame):
            grouped = grouped[columns]
        return grouped.get_group(get_key)

    else:
        # to create empty DataFrame/Series, which has the same
        # dtype as the original
        if isinstance(df, pd.DataFrame):
            # may be SeriesGroupBy
            df = df[columns]
        return df.iloc[0:0]
