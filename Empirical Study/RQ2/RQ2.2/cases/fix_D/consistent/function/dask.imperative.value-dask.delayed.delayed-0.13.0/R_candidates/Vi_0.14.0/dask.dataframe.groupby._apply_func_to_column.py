def _apply_func_to_column(df_like, column, func):
    if column is None:
        return func(df_like)

    return func(df_like[column])
