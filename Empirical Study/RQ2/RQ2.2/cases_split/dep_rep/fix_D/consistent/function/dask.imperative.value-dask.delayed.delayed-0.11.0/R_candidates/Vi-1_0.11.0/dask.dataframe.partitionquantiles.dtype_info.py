def dtype_info(df):
    info = None
    if str(df.dtype) == 'category':
        data = df.values
        info = (data.categories, data.ordered)
    return df.dtype, info
