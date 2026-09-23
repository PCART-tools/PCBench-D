def segmented_tensor(
    min_dim=1,
    max_dim=4,
    dtype=np.float32,
    is_sorted=True,
    elements=None,
    segment_generator=segment_ids,
    allow_empty=False,
    **kwargs
):
    gen_empty = st.booleans() if allow_empty else st.just(False)
    data_dims_ = st.lists(dims(**kwargs), min_size=min_dim, max_size=max_dim)
    data_dims_ = st.tuples(
        gen_empty, data_dims_
    ).map(lambda pair: ([0] if pair[0] else []) + pair[1])
    return data_dims_.flatmap(lambda data_dims: st.tuples(
        arrays(data_dims, dtype, elements),
        segment_generator(data_dims[0], is_sorted=is_sorted),
    ))
