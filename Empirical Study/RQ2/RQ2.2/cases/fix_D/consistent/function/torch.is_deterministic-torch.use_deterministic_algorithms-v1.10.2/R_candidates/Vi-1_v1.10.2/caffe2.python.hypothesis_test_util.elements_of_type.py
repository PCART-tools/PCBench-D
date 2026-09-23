def elements_of_type(dtype=np.float32, filter_=None):
    elems = None
    if dtype is np.float16:
        elems = floats(min_value=-1.0, max_value=1.0, width=16)
    elif dtype is np.float32:
        elems = floats(min_value=-1.0, max_value=1.0, width=32)
    elif dtype is np.float64:
        elems = floats(min_value=-1.0, max_value=1.0, width=64)
    elif dtype is np.int32:
        elems = st.integers(min_value=0, max_value=2 ** 31 - 1)
    elif dtype is np.int64:
        elems = st.integers(min_value=0, max_value=2 ** 63 - 1)
    elif dtype is np.bool:
        elems = st.booleans()
    else:
        raise ValueError("Unexpected dtype without elements provided")
    return elems if filter_ is None else elems.filter(filter_)
