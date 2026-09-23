def sparse_segmented_tensor(min_dim=1, max_dim=4, dtype=np.float32,
                            is_sorted=True, elements=None, allow_empty=False,
                            segment_generator=segment_ids, itype=np.int64,
                            **kwargs):
    gen_empty = st.booleans() if allow_empty else st.just(False)
    data_dims_ = st.lists(dims(**kwargs), min_size=min_dim, max_size=max_dim)
    all_dims_ = st.tuples(gen_empty, data_dims_).flatmap(
        lambda pair: st.tuples(
            st.just(pair[1]),
            (st.integers(min_value=1, max_value=pair[1][0]) if not pair[0]
             else st.just(0)),
        ))
    return all_dims_.flatmap(lambda dims: st.tuples(
        arrays(dims[0], dtype, elements),
        arrays(dims[1], dtype=itype, elements=st.integers(
            min_value=0, max_value=dims[0][0] - 1)),
        segment_generator(dims[1], is_sorted=is_sorted),
    ))
