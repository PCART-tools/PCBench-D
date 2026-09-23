def get_key(record):
    if almost_equal_schemas(record, IdList):
        key = "values"
    elif almost_equal_schemas(
        record, IdScoreList, check_field_types=False
    ):
        key = "values:keys"
    else:
        raise NotImplementedError("Not implemented for {}".format(record))
    assert record[key].metadata is not None, "Blob {} doesn't have metadata".format(
        str(record[key]())
    )
    return record[key]
