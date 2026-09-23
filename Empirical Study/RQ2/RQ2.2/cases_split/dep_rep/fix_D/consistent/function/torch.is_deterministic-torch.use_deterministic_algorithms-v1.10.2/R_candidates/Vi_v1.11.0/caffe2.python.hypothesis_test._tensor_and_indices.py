def _tensor_and_indices(min_dim=1, max_dim=4, dtype=np.float32,
                        elements=None, **kwargs):
    """ generates a tensor and a list of indices of larger tensor of same dim"""
    data_dims_ = st.lists(hu.dims(**kwargs), min_size=min_dim, max_size=max_dim)
    original_dim = st.integers(min_value=2, max_value=10)
    return st.tuples(data_dims_, original_dim).flatmap(lambda pair: st.tuples(
        st.just(pair[1]),  # original dimension
        hu.arrays(pair[0], dtype, elements),  # data tensor
        hu.arrays(pair[0][0], dtype=np.int64, elements=st.integers(
            min_value=0, max_value=pair[1] - 1)),
    ))
