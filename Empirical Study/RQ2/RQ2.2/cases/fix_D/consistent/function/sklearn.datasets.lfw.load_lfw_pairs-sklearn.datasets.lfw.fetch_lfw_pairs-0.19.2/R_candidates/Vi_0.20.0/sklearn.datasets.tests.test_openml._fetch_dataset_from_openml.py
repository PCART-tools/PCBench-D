def _fetch_dataset_from_openml(data_id, data_name, data_version,
                               target_column,
                               expected_observations, expected_features,
                               expected_missing,
                               expected_data_dtype, expected_target_dtype,
                               expect_sparse, compare_default_target):
    # fetches a dataset in three various ways from OpenML, using the
    # fetch_openml function, and does various checks on the validity of the
    # result. Note that this function can be mocked (by invoking
    # _monkey_patch_webbased_functions before invoking this function)
    data_by_name_id = fetch_openml(name=data_name, version=data_version,
                                   cache=False)
    assert int(data_by_name_id.details['id']) == data_id

    fetch_openml(name=data_name, cache=False)
    # without specifying the version, there is no guarantee that the data id
    # will be the same

    # fetch with dataset id
    data_by_id = fetch_openml(data_id=data_id, cache=False,
                              target_column=target_column)
    assert data_by_id.details['name'] == data_name
    assert data_by_id.data.shape == (expected_observations, expected_features)
    if isinstance(target_column, str):
        # single target, so target is vector
        assert data_by_id.target.shape == (expected_observations, )
    elif isinstance(target_column, list):
        # multi target, so target is array
        assert data_by_id.target.shape == (expected_observations,
                                           len(target_column))
    assert data_by_id.data.dtype == np.float64
    assert data_by_id.target.dtype == expected_target_dtype
    assert len(data_by_id.feature_names) == expected_features
    for feature in data_by_id.feature_names:
        assert isinstance(feature, string_types)

    # TODO: pass in a list of expected nominal features
    for feature, categories in data_by_id.categories.items():
        feature_idx = data_by_id.feature_names.index(feature)
        values = np.unique(data_by_id.data[:, feature_idx])
        values = values[np.isfinite(values)]
        assert set(values) <= set(range(len(categories)))

    if compare_default_target:
        # check whether the data by id and data by id target are equal
        data_by_id_default = fetch_openml(data_id=data_id, cache=False)
        if data_by_id.data.dtype == np.float64:
            np.testing.assert_allclose(data_by_id.data,
                                       data_by_id_default.data)
        else:
            assert np.array_equal(data_by_id.data, data_by_id_default.data)
        if data_by_id.target.dtype == np.float64:
            np.testing.assert_allclose(data_by_id.target,
                                       data_by_id_default.target)
        else:
            assert np.array_equal(data_by_id.target, data_by_id_default.target)

    if expect_sparse:
        assert isinstance(data_by_id.data, scipy.sparse.csr_matrix)
    else:
        assert isinstance(data_by_id.data, np.ndarray)
        # np.isnan doesn't work on CSR matrix
        assert (np.count_nonzero(np.isnan(data_by_id.data)) ==
                expected_missing)

    # test return_X_y option
    fetch_func = partial(fetch_openml, data_id=data_id, cache=False,
                         target_column=target_column)
    check_return_X_y(data_by_id, fetch_func)
    return data_by_id
