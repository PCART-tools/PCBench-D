@st.composite
def _inputs(draw):
    N = draw(st.integers(min_value=0, max_value=5))
    D = draw(st.integers(min_value=1, max_value=5))
    # N, D, data, lambda1, lambda2
    return (
        N,
        D,
        draw(st.lists(
            min_size=N * D,
            max_size=N * D,
            elements=st.one_of(
                st.floats(min_value=-10, max_value=1 - TOLERANCE),
                st.floats(min_value=1 + TOLERANCE, max_value=10))
        )),
        draw(st.lists(
            elements=st.one_of(
                st.floats(min_value=-2, max_value=-TOLERANCE),
                st.floats(min_value=TOLERANCE, max_value=2)),
            min_size=D,
            max_size=D,
        )),
        draw(st.lists(
            elements=st.floats(min_value=-2, max_value=2),
            min_size=D,
            max_size=D,
        )),
    )
