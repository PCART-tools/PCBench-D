@st.composite
def _inputs(draw):
    batch_size = draw(st.integers(2, 10))
    rows_num = draw(st.integers(1, 100))
    block_size = draw(st.integers(1, 2))
    index_num = draw(st.integers(1, 10))
    return (
        draw(hnp.arrays(
            np.float32,
            (batch_size, rows_num, block_size),
            elements=hu.floats(-10.0, 10.0),
        )),
        draw(hnp.arrays(
            np.int32,
            (index_num, 1),
            elements=st.integers(0, rows_num - 1),
        )),
    )
