def _is_id_score_list(input_record):
    return almost_equal_schemas(input_record,
                                IdScoreList,
                                check_field_types=False)
