def almost_equal_schemas(
    record,
    original_schema,
    check_field_names=True,
    check_field_types=True,
    check_field_metas=False,
):
    if original_schema == IdList:
        return schema.equal_schemas(
            record,
            IdList,
            check_field_names=check_field_names,
            check_field_types=check_field_types,
            check_field_metas=check_field_metas,
        ) or schema.equal_schemas(
            record,
            IdListWithEvicted,
            check_field_names=check_field_names,
            check_field_types=check_field_types,
            check_field_metas=check_field_metas,
        )
    elif original_schema == IdScoreList:
        return schema.equal_schemas(
            record,
            IdScoreList,
            check_field_names=check_field_names,
            check_field_types=check_field_types,
            check_field_metas=check_field_metas,
        ) or schema.equal_schemas(
            record,
            IdScoreListWithEvicted,
            check_field_names=check_field_names,
            check_field_types=check_field_types,
            check_field_metas=check_field_metas,
        )
    else:
        return schema.equal_schemas(record, original_schema)
