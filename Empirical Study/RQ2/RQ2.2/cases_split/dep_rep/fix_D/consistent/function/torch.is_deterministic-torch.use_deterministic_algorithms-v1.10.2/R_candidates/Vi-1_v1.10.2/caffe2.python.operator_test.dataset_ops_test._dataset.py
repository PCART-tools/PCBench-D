@st.composite
def _dataset(draw, min_elements=3, max_elements=10, **kwargs):
    schema = Struct(
        # Dense Features Map
        ("floats", Map(Scalar(np.int32), Scalar(np.float32))),
        # Sparse Features Map
        (
            "int_lists",
            Map(
                Scalar(np.int32),
                List(Scalar(np.int64)),
            ),
        ),
        # Complex Type
        ("text", Scalar(str)),
    )

    num_records = draw(st.integers(min_value=min_elements, max_value=max_elements))

    raw_dense_features_map_contents = draw(_dense_features_map(num_records))

    raw_sparse_features_map_contents = draw(_sparse_features_map(num_records))

    raw_text_contents = [
        draw(
            st.lists(
                st.text(alphabet=string.ascii_lowercase),
                min_size=num_records,
                max_size=num_records,
            )
        )
    ]

    # Concatenate all raw contents to a single one
    contents_raw = (
        raw_dense_features_map_contents
        + raw_sparse_features_map_contents
        + raw_text_contents
    )

    contents = from_blob_list(schema, contents_raw)

    return (schema, contents, num_records)
