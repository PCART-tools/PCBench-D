def schema_check(schema, previous=None):
    record = as_record(schema)
    if previous is not None:
        assert equal_schemas(schema, previous)
    return record
