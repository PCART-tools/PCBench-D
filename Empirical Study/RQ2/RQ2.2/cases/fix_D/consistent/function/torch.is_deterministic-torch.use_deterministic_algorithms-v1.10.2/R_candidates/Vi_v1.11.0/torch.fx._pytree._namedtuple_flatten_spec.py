def _namedtuple_flatten_spec(d: NamedTuple, spec: TreeSpec) -> List[Any]:
    return [d[i] for i in range(len(spec.children_specs))]
