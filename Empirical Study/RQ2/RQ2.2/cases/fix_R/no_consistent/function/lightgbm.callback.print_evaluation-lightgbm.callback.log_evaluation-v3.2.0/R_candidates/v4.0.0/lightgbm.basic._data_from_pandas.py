def _data_from_pandas(
    data,
    feature_name: Optional[_LGBM_FeatureNameConfiguration],
    categorical_feature: Optional[_LGBM_CategoricalFeatureConfiguration],
    pandas_categorical: Optional[List[List]]
):
    if isinstance(data, pd_DataFrame):
        if len(data.shape) != 2 or data.shape[0] < 1:
            raise ValueError('Input data must be 2 dimensional and non empty.')
        if feature_name == 'auto' or feature_name is None:
            data = data.rename(columns=str, copy=False)
        cat_cols = [col for col, dtype in zip(data.columns, data.dtypes) if isinstance(dtype, pd_CategoricalDtype)]
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
            data = data.copy(deep=False)  # not alter origin DataFrame
            data[cat_cols] = data[cat_cols].apply(lambda x: x.cat.codes).replace({-1: np.nan})
        if categorical_feature is not None:
            if feature_name is None:
                feature_name = list(data.columns)
            if categorical_feature == 'auto':  # use cat cols from DataFrame
                categorical_feature = cat_cols_not_ordered
            else:  # use cat cols specified by user
                categorical_feature = list(categorical_feature)  # type: ignore[assignment]
        if feature_name == 'auto':
            feature_name = list(data.columns)
        _check_for_bad_pandas_dtypes(data.dtypes)
        df_dtypes = [dtype.type for dtype in data.dtypes]
        df_dtypes.append(np.float32)  # so that the target dtype considers floats
        target_dtype = np.find_common_type(df_dtypes, [])
        try:
            # most common case (no nullable dtypes)
            data = data.to_numpy(dtype=target_dtype, copy=False)
        except TypeError:
            # 1.0 <= pd version < 1.1 and nullable dtypes, least common case
            # raises error because array is casted to type(pd.NA) and there's no na_value argument
            data = data.astype(target_dtype, copy=False).values
        except ValueError:
            # data has nullable dtypes, but we can specify na_value argument and copy will be made
            data = data.to_numpy(dtype=target_dtype, na_value=np.nan)
    else:
        if feature_name == 'auto':
            feature_name = None
        if categorical_feature == 'auto':
            categorical_feature = None
    return data, feature_name, categorical_feature, pandas_categorical
