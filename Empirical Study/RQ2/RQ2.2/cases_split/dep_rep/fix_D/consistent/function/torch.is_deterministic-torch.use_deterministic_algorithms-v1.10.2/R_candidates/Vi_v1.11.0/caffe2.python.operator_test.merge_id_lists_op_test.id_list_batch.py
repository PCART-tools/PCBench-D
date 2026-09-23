@st.composite
def id_list_batch(draw):
    num_inputs = draw(st.integers(1, 3))
    batch_size = draw(st.integers(5, 10))
    values_dtype = draw(st.sampled_from([np.int32, np.int64]))
    inputs = []
    for _ in range(num_inputs):
        size = draw(st.integers(5, 10))
        values = draw(hnp.arrays(values_dtype, size, st.integers(1, 10)))
        lengths = draw(hu.lengths(len(values),
                                  min_segments=batch_size,
                                  max_segments=batch_size))
        inputs.append(lengths)
        inputs.append(values)
    return inputs
