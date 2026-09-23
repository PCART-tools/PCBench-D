def _gen_test_add_padding(with_pad_data=True,
                          is_remove=False):
    def gen_with_size(args):
        lengths, inner_shape = args
        data_dim = [sum(lengths)] + inner_shape
        lengths = np.array(lengths, dtype=np.int32)
        if with_pad_data:
            return st.tuples(
                st.just(lengths),
                hu.arrays(data_dim),
                hu.arrays(inner_shape),
                hu.arrays(inner_shape))
        else:
            return st.tuples(st.just(lengths), hu.arrays(data_dim))

    min_len = 4 if is_remove else 0
    lengths = st.lists(
        st.integers(min_value=min_len, max_value=10),
        min_size=0,
        max_size=5)
    inner_shape = st.lists(
        st.integers(min_value=1, max_value=3),
        min_size=0,
        max_size=2)
    return st.tuples(lengths, inner_shape).flatmap(gen_with_size)
