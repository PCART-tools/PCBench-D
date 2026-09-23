@st.composite
def _bad_tensor_splits(draw):
    lengths = draw(st.lists(st.integers(4, 6), min_size=4, max_size=4))
    batch_size = 4
    element_pairs = [
        (batch, r) for batch in range(batch_size) for r in range(len(lengths))
    ]
    perm = draw(st.permutations(element_pairs))
    ranges = [[(0, 0)] * len(lengths) for _ in range(batch_size)]
    offset = 0

    # Inject some bad samples depending on the batch.
    # Batch 2: length is set to 0. This way, 25% of the samples are empty.
    # Batch 0-1: length is set to half the original length. This way, 50% of the
    # samples are of mismatched length.
    for pair in perm:
        if pair[0] == 2:
            length = 0
        elif pair[0] <= 1:
            length = lengths[pair[1]] // 2
        else:
            length = lengths[pair[1]]
        ranges[pair[0]][pair[1]] = (offset, length)
        offset += length

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
