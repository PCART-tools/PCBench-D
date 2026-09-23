@st.composite
def _glu_old_input(draw):
    dims = draw(st.lists(st.integers(min_value=1, max_value=5), min_size=1, max_size=3))
    axis = draw(st.integers(min_value=0, max_value=len(dims)))
    # The axis dimension must be divisible by two
    axis_dim = 2 * draw(st.integers(min_value=1, max_value=2))
    dims.insert(axis, axis_dim)
    X = draw(hu.arrays(dims, np.float32, None))
    return (X, axis)
