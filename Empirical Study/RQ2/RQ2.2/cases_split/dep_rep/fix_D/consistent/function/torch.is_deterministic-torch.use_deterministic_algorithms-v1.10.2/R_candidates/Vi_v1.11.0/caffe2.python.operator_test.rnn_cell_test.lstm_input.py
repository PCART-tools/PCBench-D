def lstm_input():
    '''
    Create input tensor where each dimension is from 1 to 4, ndim=3 and
    last dimension size is a factor of 4
    '''
    dims_ = st.tuples(
        st.integers(min_value=1, max_value=4),  # t
        st.integers(min_value=1, max_value=4),  # n
        st.integers(min_value=1, max_value=4),  # d
    )

    def create_input(dims):
        dims = list(dims)
        dims[2] *= 4
        return hu.arrays(dims)

    return dims_.flatmap(create_input)
