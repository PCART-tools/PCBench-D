def _dtypes(dtypes=None):
    dtypes = dtypes if dtypes else [np.int32, np.int64, np.float32]
    return st.sampled_from(dtypes)
