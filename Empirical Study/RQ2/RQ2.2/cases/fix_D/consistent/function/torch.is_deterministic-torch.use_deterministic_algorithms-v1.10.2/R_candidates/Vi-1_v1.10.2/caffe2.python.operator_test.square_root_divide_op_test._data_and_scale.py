def _data_and_scale(
        data_min_size=4, data_max_size=10,
        examples_min_number=1, examples_max_number=4,
        dtype=np.float32, elements=None):
    params_ = st.tuples(
        st.integers(min_value=examples_min_number,
                    max_value=examples_max_number),
        st.integers(min_value=data_min_size,
                    max_value=data_max_size),
        st.sampled_from([np.float32, np.int32, np.int64])
    )
    return params_.flatmap(
        lambda param_: st.tuples(
            hu.arrays([param_[0], param_[1]], dtype=dtype),
            hu.arrays(
                [param_[0]], dtype=param_[2],
                elements=(hu.floats(0.0, 10000.0) if param_[2] in [np.float32]
                          else st.integers(0, 10000)),
            ),
        )
    )
