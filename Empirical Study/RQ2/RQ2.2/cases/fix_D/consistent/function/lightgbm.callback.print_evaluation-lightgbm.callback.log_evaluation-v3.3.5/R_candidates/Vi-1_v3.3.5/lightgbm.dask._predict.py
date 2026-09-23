def _predict(
    model: LGBMModel,
    data: _DaskMatrixLike,
    client: Client,
    raw_score: bool = False,
    pred_proba: bool = False,
    pred_leaf: bool = False,
    pred_contrib: bool = False,
    dtype: _PredictionDtype = np.float32,
    **kwargs: Any
) -> Union[dask_Array, List[dask_Array]]:
    """Inner predict routine.

    Parameters
    ----------
    model : lightgbm.LGBMClassifier, lightgbm.LGBMRegressor, or lightgbm.LGBMRanker class
        Fitted underlying model.
    data : Dask Array or Dask DataFrame of shape = [n_samples, n_features]
        Input feature matrix.
    raw_score : bool, optional (default=False)
        Whether to predict raw scores.
    pred_proba : bool, optional (default=False)
        Should method return results of ``predict_proba`` (``pred_proba=True``) or ``predict`` (``pred_proba=False``).
    pred_leaf : bool, optional (default=False)
        Whether to predict leaf index.
    pred_contrib : bool, optional (default=False)
        Whether to predict feature contributions.
    dtype : np.dtype, optional (default=np.float32)
        Dtype of the output.
    **kwargs
        Other parameters passed to ``predict`` or ``predict_proba`` method.

    Returns
    -------
    predicted_result : Dask Array of shape = [n_samples] or shape = [n_samples, n_classes]
        The predicted values.
    X_leaves : Dask Array of shape = [n_samples, n_trees] or shape = [n_samples, n_trees * n_classes]
        If ``pred_leaf=True``, the predicted leaf of every tree for each sample.
    X_SHAP_values : Dask Array of shape = [n_samples, n_features + 1] or shape = [n_samples, (n_features + 1) * n_classes] or (if multi-class and using sparse inputs) a list of ``n_classes`` Dask Arrays of shape = [n_samples, n_features + 1]
        If ``pred_contrib=True``, the feature contributions for each sample.
    """
    if not all((DASK_INSTALLED, PANDAS_INSTALLED, SKLEARN_INSTALLED)):
        raise LightGBMError('dask, pandas and scikit-learn are required for lightgbm.dask')
    if isinstance(data, dask_DataFrame):
        return data.map_partitions(
            _predict_part,
            model=model,
            raw_score=raw_score,
            pred_proba=pred_proba,
            pred_leaf=pred_leaf,
            pred_contrib=pred_contrib,
            **kwargs
        ).values
    elif isinstance(data, dask_Array):
        # for multi-class classification with sparse matrices, pred_contrib predictions
        # are returned as a list of sparse matrices (one per class)
        num_classes = model._n_classes or -1

        if (
            num_classes > 2
            and pred_contrib
            and isinstance(data._meta, ss.spmatrix)
        ):

            predict_function = partial(
                _predict_part,
                model=model,
                raw_score=False,
                pred_proba=pred_proba,
                pred_leaf=False,
                pred_contrib=True,
                **kwargs
            )

            delayed_chunks = data.to_delayed()
            bag = dask_bag_from_delayed(delayed_chunks[:, 0])

            @delayed
            def _extract(items: List[Any], i: int) -> Any:
                return items[i]

            preds = bag.map_partitions(predict_function)

            # pred_contrib output will have one column per feature,
            # plus one more for the base value
            num_cols = model.n_features_ + 1

            nrows_per_chunk = data.chunks[0]
            out = [[] for _ in range(num_classes)]

            # need to tell Dask the expected type and shape of individual preds
            pred_meta = data._meta

            for j, partition in enumerate(preds.to_delayed()):
                for i in range(num_classes):
                    part = dask_array_from_delayed(
                        value=_extract(partition, i),
                        shape=(nrows_per_chunk[j], num_cols),
                        meta=pred_meta
                    )
                    out[i].append(part)

            # by default, dask.array.concatenate() concatenates sparse arrays into a COO matrix
            # the code below is used instead to ensure that the sparse type is preserved during concatentation
            if isinstance(pred_meta, ss.csr_matrix):
                concat_fn = partial(ss.vstack, format='csr')
            elif isinstance(pred_meta, ss.csc_matrix):
                concat_fn = partial(ss.vstack, format='csc')
            else:
                concat_fn = ss.vstack

            # At this point, `out` is a list of lists of delayeds (each of which points to a matrix).
            # Concatenate them to return a list of Dask Arrays.
            for i in range(num_classes):
                out[i] = dask_array_from_delayed(
                    value=delayed(concat_fn)(out[i]),
                    shape=(data.shape[0], num_cols),
                    meta=pred_meta
                )

            return out

        data_row = client.compute(data[[0]]).result()
        predict_fn = partial(
            _predict_part,
            model=model,
            raw_score=raw_score,
            pred_proba=pred_proba,
            pred_leaf=pred_leaf,
            pred_contrib=pred_contrib,
            **kwargs,
        )
        pred_row = predict_fn(data_row)
        chunks = (data.chunks[0],)
        map_blocks_kwargs = {}
        if len(pred_row.shape) > 1:
            chunks += (pred_row.shape[1],)
        else:
            map_blocks_kwargs['drop_axis'] = 1
        return data.map_blocks(
            predict_fn,
            chunks=chunks,
            meta=pred_row,
            dtype=dtype,
            **map_blocks_kwargs,
        )
    else:
        raise TypeError(f'Data must be either Dask Array or Dask DataFrame. Got {type(data).__name__}.')
