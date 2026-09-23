@deprecate_function(
    "Use `assert_frame_equal` instead and pass `categorical_as_str=True`.",
    version="0.18.13",
)
def assert_frame_equal_local_categoricals(df_a: DataFrame, df_b: DataFrame) -> None:
    """Assert frame equal for frames containing categoricals."""
    for (a_name, a_value), (b_name, b_value) in zip(
        df_a.schema.items(), df_b.schema.items()
    ):
        if a_name != b_name:
            print(f"{a_name} != {b_name}")
            raise AssertionError
        if a_value != b_value:
            print(f"{a_value} != {b_value}")
            raise AssertionError

    cat_to_str = F.col(Categorical).cast(str)
    assert_frame_equal(df_a.with_columns(cat_to_str), df_b.with_columns(cat_to_str))
    cat_to_phys = F.col(Categorical).to_physical()
    assert_frame_equal(df_a.with_columns(cat_to_phys), df_b.with_columns(cat_to_phys))
