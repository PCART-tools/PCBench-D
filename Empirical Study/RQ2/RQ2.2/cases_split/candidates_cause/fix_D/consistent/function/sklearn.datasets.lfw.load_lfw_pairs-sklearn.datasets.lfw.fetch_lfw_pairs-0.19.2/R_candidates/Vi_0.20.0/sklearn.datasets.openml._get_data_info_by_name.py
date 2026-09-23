def _get_data_info_by_name(name, version, data_home):
    """
    Utilizes the openml dataset listing api to find a dataset by
    name/version
    OpenML api function:
    https://www.openml.org/api_docs#!/data/get_data_list_data_name_data_name

    Parameters
    ----------
    name : str
        name of the dataset

    version : int or str
        If version is an integer, the exact name/version will be obtained from
        OpenML. If version is a string (value: "active") it will take the first
        version from OpenML that is annotated as active. Any other string
        values except "active" are treated as integer.

    data_home : str or None
        Location to cache the response. None if no cache is required.

    Returns
    -------
    first_dataset : json
        json representation of the first dataset object that adhired to the
        search criteria

    """
    if version == "active":
        # situation in which we return the oldest active version
        url = _SEARCH_NAME.format(name) + "/status/active/"
        error_msg = "No active dataset {} found.".format(name)
        json_data = _get_json_content_from_openml_api(url, error_msg, True,
                                                      data_home)
        res = json_data['data']['dataset']
        if len(res) > 1:
            warn("Multiple active versions of the dataset matching the name"
                 " {name} exist. Versions may be fundamentally different, "
                 "returning version"
                 " {version}.".format(name=name, version=res[0]['version']))
        return res[0]

    # an integer version has been provided
    url = (_SEARCH_NAME + "/data_version/{}").format(name, version)
    json_data = _get_json_content_from_openml_api(url, None, False,
                                                  data_home)
    if json_data is None:
        # we can do this in 1 function call if OpenML does not require the
        # specification of the dataset status (i.e., return datasets with a
        # given name / version regardless of active, deactivated, etc. )
        # TODO: feature request OpenML.
        url += "/status/deactivated"
        error_msg = "Dataset {} with version {} not found.".format(name,
                                                                   version)
        json_data = _get_json_content_from_openml_api(url, error_msg, True,
                                                      data_home)

    return json_data['data']['dataset'][0]
