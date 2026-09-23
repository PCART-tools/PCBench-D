def is_categorical_dtype(arr_or_dtype):
    if hasattr(arr_or_dtype,'dtype'):
        arr_or_dtype = arr_or_dtype.dtype

    if isinstance(arr_or_dtype, CategoricalDtype):
        return True
    try:
        return arr_or_dtype == 'category'
    except:
        return False
