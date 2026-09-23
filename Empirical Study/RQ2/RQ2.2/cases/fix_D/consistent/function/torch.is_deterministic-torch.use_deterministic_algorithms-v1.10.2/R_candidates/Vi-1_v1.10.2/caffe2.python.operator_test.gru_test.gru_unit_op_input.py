def gru_unit_op_input():
    '''
    Create input tensor where each dimension is from 1 to 4, ndim=3 and
    last dimension size is a factor of 3

    hidden_t_prev.shape     = (1, N, D)
    '''
    dims_ = st.tuples(
        st.integers(min_value=1, max_value=1),  # 1, one timestep
        st.integers(min_value=1, max_value=4),  # n
        st.integers(min_value=1, max_value=4),  # d
    )

    def create_input(dims):
        dims = list(dims)
        dims[2] *= 3
        return hu.arrays(dims)

    return dims_.flatmap(create_input)
