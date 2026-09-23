def _test_features_list(data_id):
    # XXX Test is intended to verify/ensure correct decoding behavior
    # Not usable with sparse data or datasets that have columns marked as
    # {row_identifier, ignore}
    def decode_column(data_bunch, col_idx):
        col_name = data_bunch.feature_names[col_idx]
        if col_name in data_bunch.categories:
            # XXX: This would be faster with np.take, although it does not
            # handle missing values fast (also not with mode='wrap')
            cat = data_bunch.categories[col_name]
            result = [cat[idx] if 0 <= idx < len(cat) else None for idx in
                      data_bunch.data[:, col_idx].astype(int)]
            return np.array(result, dtype='O')
        else:
            # non-nominal attribute
            return data_bunch.data[:, col_idx]

    data_bunch = fetch_openml(data_id=data_id, cache=False, target_column=None)

    # also obtain decoded arff
    data_description = _get_data_description_by_id(data_id, None)
    sparse = data_description['format'].lower() == 'sparse_arff'
    if sparse is True:
        raise ValueError('This test is not intended for sparse data, to keep '
                         'code relatively simple')
    data_arff = _download_data_arff(data_description['file_id'],
                                    sparse, None, False)
    data_downloaded = np.array(data_arff['data'], dtype='O')

    for i in range(len(data_bunch.feature_names)):
        # XXX: Test per column, as this makes it easier to avoid problems with
        # missing values

        np.testing.assert_array_equal(data_downloaded[:, i],
                                      decode_column(data_bunch, i))
