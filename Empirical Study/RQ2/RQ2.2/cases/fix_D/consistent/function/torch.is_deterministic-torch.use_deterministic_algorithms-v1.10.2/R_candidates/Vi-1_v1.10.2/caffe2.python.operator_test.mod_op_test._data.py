@st.composite
def _data(draw):
    return draw(
        hu.tensor(
            dtype=np.int64,
            elements=st.integers(
                min_value=np.iinfo(np.int64).min, max_value=np.iinfo(np.int64).max
            )
        )
    )
