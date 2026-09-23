def load_op_deps(fname: str) -> Any:
    with open(fname, 'r') as stream:
        return yaml.safe_load(stream)
