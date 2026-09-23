@st.composite
def _dense_features_map(draw, num_records, **kwargs):
    float_lengths = draw(
        st.lists(
            st.integers(min_value=1, max_value=10),
            min_size=num_records,
            max_size=num_records,
        )
    )

    total_length = sum(float_lengths)

    float_keys = draw(
        st.lists(
            st.integers(min_value=1, max_value=100),
            min_size=total_length,
            max_size=total_length,
            unique=True,
        )
    )

    float_values = draw(
        st.lists(st.floats(), min_size=total_length, max_size=total_length)
    )

    return [float_lengths, float_keys, float_values]
