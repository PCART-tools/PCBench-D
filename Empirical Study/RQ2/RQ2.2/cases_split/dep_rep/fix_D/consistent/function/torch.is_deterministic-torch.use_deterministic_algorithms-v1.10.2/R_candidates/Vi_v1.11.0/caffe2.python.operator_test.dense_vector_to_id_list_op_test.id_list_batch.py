@st.composite
def id_list_batch(draw):
    batch_size = draw(st.integers(2, 2))
    values_dtype = np.float32
    inputs = []
    sample_size = draw(st.integers(5, 10))
    for _ in range(batch_size):
        values = draw(hnp.arrays(values_dtype, sample_size, st.integers(0, 1)))
        inputs += [values]
    return [np.array(inputs)]
