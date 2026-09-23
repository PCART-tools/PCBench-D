def _dict_flatten_spec(d: Dict[Any, Any], spec: TreeSpec) -> List[Any]:
    return list([d[k] for k in spec.context])
