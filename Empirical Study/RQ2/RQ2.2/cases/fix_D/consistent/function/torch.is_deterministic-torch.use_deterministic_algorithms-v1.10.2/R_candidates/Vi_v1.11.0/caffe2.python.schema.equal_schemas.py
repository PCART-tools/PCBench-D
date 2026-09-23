def equal_schemas(schema,
                  original_schema,
                  check_field_names=True,
                  check_field_types=True,
                  check_field_metas=False):
    assert isinstance(schema, Field)
    assert isinstance(original_schema, Field)

    if check_field_names and (
            schema.field_names() != original_schema.field_names()):
        return False
    if check_field_types and (
            schema.field_types() != original_schema.field_types()):
        return False
    if check_field_metas and (
            schema.field_metadata() != original_schema.field_metadata()):
        return False

    return True
