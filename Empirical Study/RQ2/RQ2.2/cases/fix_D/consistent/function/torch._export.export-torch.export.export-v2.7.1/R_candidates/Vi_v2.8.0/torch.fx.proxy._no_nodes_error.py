def _no_nodes_error(arg):
    raise RuntimeError(
        "Keys for dictionaries used as an argument cannot contain a "
        f"Node. Got key: {arg}"
    )
