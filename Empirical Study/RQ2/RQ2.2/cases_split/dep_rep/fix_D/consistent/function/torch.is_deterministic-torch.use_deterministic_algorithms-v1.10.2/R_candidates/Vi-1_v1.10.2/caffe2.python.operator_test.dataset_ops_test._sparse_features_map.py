@st.composite
def _sparse_features_map(draw, num_records, **kwargs):
    sparse_maps_lengths = draw(
        st.lists(
            st.integers(min_value=1, max_value=10),
            min_size=num_records,
            max_size=num_records,
        )
    )

    sparse_maps_total_length = sum(sparse_maps_lengths)

    sparse_keys = draw(
        st.lists(
            st.integers(min_value=1, max_value=100),
            min_size=sparse_maps_total_length,
            max_size=sparse_maps_total_length,
            unique=True,
        )
    )

    sparse_values_lengths = draw(
        st.lists(
            st.integers(min_value=1, max_value=10),
            min_size=sparse_maps_total_length,
            max_size=sparse_maps_total_length,
        )
    )

    total_sparse_values_lengths = sum(sparse_values_lengths)

    sparse_values = draw(
        # max_value is max int64
        st.lists(
            st.integers(min_value=1, max_value=9223372036854775807),
            min_size=total_sparse_values_lengths,
            max_size=total_sparse_values_lengths,
        )
    )

    return [
        sparse_maps_lengths,
        sparse_keys,
        sparse_values_lengths,
        sparse_values,
    ]
