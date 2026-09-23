def _data_from_pandas(data, feature_name, categorical_feature, pandas_categorical):
    if isinstance(data, pd_DataFrame):
        if len(data.shape) != 2 or data.shape[0] < 1:
            raise ValueError('Input data must be 2 dimensional and non empty.')
        if feature_name == 'auto' or feature_name is None:
            data = data.rename(columns=str)
        cat_cols = list(data.select_dtypes(include=['category']).columns)
        cat_cols_not_ordered = [col for col in cat_cols if not data[col].cat.ordered]
        if pandas_categorical is None:  # train dataset
            pandas_categorical = [list(data[col].cat.categories) for col in cat_cols]
        else:
            if len(cat_cols) != len(pandas_categorical):
                raise ValueError('train and valid dataset categorical_feature do not match.')
            for col, category in zip(cat_cols, pandas_categorical):
                if list(data[col].cat.categories) != list(category):
                    data[col] = data[col].cat.set_categories(category)
        if len(cat_cols):  # cat_cols is list
            data = data.copy()  # not alter origin DataFrame
            data[cat_cols] = data[cat_cols].apply(lambda x: x.cat.codes).replace({-1: np.nan})
        if categorical_feature is not None:
            if feature_name is None:
                feature_name = list(data.columns)
            if categorical_feature == 'auto':  # use cat cols from DataFrame
                categorical_feature = cat_cols_not_ordered
            else:  # use cat cols specified by user
                categorical_feature = list(categorical_feature)
        if feature_name == 'auto':
            feature_name = list(data.columns)
        bad_indices = _get_bad_pandas_dtypes(data.dtypes)
        if bad_indices:
            bad_index_cols_str = ', '.join(data.columns[bad_indices])
            raise ValueError("DataFrame.dtypes for data must be int, float or bool.\n"
                             "Did not expect the data types in the following fields: "
                             f"{bad_index_cols_str}")
        data = data.values
        if data.dtype != np.float32 and data.dtype != np.float64:
            data = data.astype(np.float32)
    else:
        if feature_name == 'auto':
            feature_name = None
        if categorical_feature == 'auto':
            categorical_feature = None
    return data, feature_name, categorical_feature, pandas_categorical
