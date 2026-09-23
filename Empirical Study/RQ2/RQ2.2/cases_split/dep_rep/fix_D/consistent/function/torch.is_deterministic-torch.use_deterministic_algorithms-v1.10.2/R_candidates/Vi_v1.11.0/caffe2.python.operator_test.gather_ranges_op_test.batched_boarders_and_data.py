def batched_boarders_and_data(
    data_min_size=5,
    data_max_size=10,
    examples_min_number=1,
    examples_max_number=4,
    example_min_size=1,
    example_max_size=3,
    dtype=np.float32,
    elements=None,
):
    dims_ = st.tuples(
        st.integers(min_value=data_min_size, max_value=data_max_size),
        st.integers(min_value=examples_min_number, max_value=examples_max_number),
        st.integers(min_value=example_min_size, max_value=example_max_size),
    )
    return dims_.flatmap(
        lambda dims: st.tuples(
            hu.arrays(
                [dims[1], dims[2], 2],
                dtype=np.int32,
                elements=st.integers(min_value=0, max_value=dims[0]),
            ),
            hu.arrays([dims[0]], dtype, elements),
        )
    )
