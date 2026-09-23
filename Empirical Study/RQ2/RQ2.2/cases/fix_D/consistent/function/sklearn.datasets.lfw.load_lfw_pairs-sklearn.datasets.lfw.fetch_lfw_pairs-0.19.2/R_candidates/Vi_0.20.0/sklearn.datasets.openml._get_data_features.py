def _get_data_features(data_id, data_home):
    # OpenML function:
    # https://www.openml.org/api_docs#!/data/get_data_features_id
    url = _DATA_FEATURES.format(data_id)
    error_message = "Dataset with data_id {} not found.".format(data_id)
    json_data = _get_json_content_from_openml_api(url, error_message, True,
                                                  data_home)
    return json_data['data_features']['feature']
