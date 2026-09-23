def is_schema_subset(schema, original_schema):
    # TODO add more checks
    return set(schema.field_names()).issubset(
        set(original_schema.field_names()))
