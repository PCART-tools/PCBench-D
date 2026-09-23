def _predict_part(
    part: _DaskPart,
    model: LGBMModel,
    raw_score: bool,
    pred_proba: bool,
    pred_leaf: bool,
    pred_contrib: bool,
    **kwargs: Any
) -> _DaskPart:

    if part.shape[0] == 0:
        result = np.array([])
    elif pred_proba:
        result = model.predict_proba(
            part,
            raw_score=raw_score,
            pred_leaf=pred_leaf,
            pred_contrib=pred_contrib,
            **kwargs
        )
    else:
        result = model.predict(
            part,
            raw_score=raw_score,
            pred_leaf=pred_leaf,
            pred_contrib=pred_contrib,
            **kwargs
        )

    # dask.DataFrame.map_partitions() expects each call to return a pandas DataFrame or Series
    if isinstance(part, pd_DataFrame):
        if len(result.shape) == 2:
            result = pd_DataFrame(result, index=part.index)
        else:
            result = pd_Series(result, index=part.index, name='predictions')

    return result
