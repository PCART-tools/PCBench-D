def _one_hots():
    index_size = st.integers(min_value=1, max_value=5)
    lengths = st.lists(
        elements=st.integers(min_value=0, max_value=5))
    return st.tuples(index_size, lengths).flatmap(
        lambda x: st.tuples(
            st.just(x[0]),
            st.just(x[1]),
            st.lists(
                elements=st.integers(min_value=0, max_value=x[0] - 1),
                min_size=sum(x[1]),
                max_size=sum(x[1]))))
