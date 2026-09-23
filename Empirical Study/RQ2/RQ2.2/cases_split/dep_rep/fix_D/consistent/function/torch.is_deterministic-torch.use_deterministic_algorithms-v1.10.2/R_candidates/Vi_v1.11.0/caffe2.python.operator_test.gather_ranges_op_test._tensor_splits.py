@st.composite
def _tensor_splits(draw):
    lengths = draw(st.lists(st.integers(1, 5), min_size=1, max_size=10))
    batch_size = draw(st.integers(1, 5))
    element_pairs = [
        (batch, r) for batch in range(batch_size) for r in range(len(lengths))
    ]
    perm = draw(st.permutations(element_pairs))
    perm = perm[:-1]  # skip one range
    ranges = [[(0, 0)] * len(lengths) for _ in range(batch_size)]
    offset = 0
    for pair in perm:
        ranges[pair[0]][pair[1]] = (offset, lengths[pair[1]])
        offset += lengths[pair[1]]

    data = draw(
        st.lists(
            st.floats(min_value=-1.0, max_value=1.0), min_size=offset, max_size=offset
        )
    )

    key = draw(st.permutations(range(offset)))

    return (
        np.array(data).astype(np.float32),
        np.array(ranges),
        np.array(lengths),
        np.array(key).astype(np.int64),
    )
