def _agg_cv_result(
    raw_results: List[List[Tuple[str, str, float, bool]]]
) -> List[Tuple[str, str, float, bool, float]]:
    """Aggregate cross-validation results."""
    cvmap: Dict[str, List[float]] = collections.OrderedDict()
    metric_type: Dict[str, bool] = {}
    for one_result in raw_results:
        for one_line in one_result:
            key = f"{one_line[0]} {one_line[1]}"
            metric_type[key] = one_line[3]
            cvmap.setdefault(key, [])
            cvmap[key].append(one_line[2])
    return [('cv_agg', k, np.mean(v), metric_type[k], np.std(v)) for k, v in cvmap.items()]
