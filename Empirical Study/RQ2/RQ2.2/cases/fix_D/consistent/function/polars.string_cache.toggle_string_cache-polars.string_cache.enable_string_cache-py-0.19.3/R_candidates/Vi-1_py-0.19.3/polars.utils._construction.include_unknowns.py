def include_unknowns(
    schema: SchemaDict, cols: Sequence[str]
) -> MutableMapping[str, PolarsDataType]:
    """Complete partial schema dict by including Unknown type."""
    return {
        col: (schema.get(col, Unknown) or Unknown)  # type: ignore[truthy-bool]
        for col in cols
    }
