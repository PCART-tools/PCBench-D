def load_root_ops(fname: str) -> List[str]:
    result = []
    with open(fname, 'r') as stream:
        for op in yaml.safe_load(stream):
            result.append(canonical_name(op))
    return result
